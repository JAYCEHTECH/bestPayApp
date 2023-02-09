import json

import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from bestPayApp import models, helper


def checkout(request):
    if request.method == "POST":
        amount = 0.49
        client_ref = helper.ref_generator(2)
        provider = "Shop Payment"

        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        return_url = f"http://127.0.0.1:8000/place_order/{client_ref}/{first_name}/{last_name}/{email}/{phone}/{address}"

        response = helper.execute_payment(amount, client_ref, provider, return_url)

        data = response.json()

        if data["status"] == "Success":
            print("trueeeeeeeeee")
            print("===============================")
            checkout_url = data['data']['checkoutUrl']
            print(checkout_url)
            return redirect(checkout_url)
        else:
            return redirect('failed')

    raw_cart = models.Cart.objects.filter(user=request.user)
    for item in raw_cart:
        if item.product_qty > item.product.quantity:
            models.Cart.objects.delete(id=item.id)
    cart_items = models.Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.product.selling_price * item.product_qty

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'shop/checkout/checkout.html', context)


def make_payment(request):
    ...


def place_order(request, client_ref, first_name, last_name, email, phone, address):
    current_user = request.user
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": "8f56b7ea-e1d0-4ce7-ace0-162f7dc55a39"
    }
    webhook_response = requests.request("GET",
                                        "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/"
                                        "requests?sorting=newest",
                                        headers=headers)

    for request in webhook_response.json()['data']:
        try:
            try:
                content = json.loads(request["content"])
            except ValueError:
                return redirect(
                    f'http://127.0.0.1:8000/place_order/{client_ref}/{first_name}/{last_name}/{email}/{phone}/{address}')
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            new_order_items = models.Cart.objects.filter(user=current_user)
            price = 0
            for item in new_order_items:
                price += item.product.selling_price

            new_order = models.Order()
            new_order.user = current_user
            new_order.order_name = f"{first_name} {last_name}"
            new_order.email = email
            new_order.phone = phone
            new_order.address = address
            new_order.payment_reference = client_ref

            cart = models.Cart.objects.filter(user=current_user)
            cart_total_price = 0
            for item in cart:
                cart_total_price += item.product.selling_price * item.product_qty
            new_order.total_price = cart_total_price
            track_no = helper.ref_generator(2)
            while models.Order.objects.filter(tracking_number=track_no) is None:
                track_no = helper.ref_generator(2)
            new_order.tracking_number = track_no

            new_order.save()

            for item in new_order_items:
                models.OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    tracking_number=track_no,
                    price=item.product.selling_price,
                    quantity=item.product_qty
                )

                order_product = models.Product.objects.filter(id=item.product_id).first()
                order_product.quantity -= item.product_qty
                order_product.save()

            messages.success(request, "Your order has been placed")
            models.Cart.objects.filter(user=current_user).delete()
            return redirect('products')
        else:
            return redirect('failed')
    return redirect('products')
