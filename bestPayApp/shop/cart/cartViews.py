from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from bestPayApp import models


@login_required(login_url='login')
def view_cart(request):
    cart = models.Cart.objects.filter(user=request.user)
    context = {'cart': cart}
    return render(request, 'shop/cart/cart.html', context)


def add_to_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = int(request.POST.get("product_id"))
            prod_qty = int(request.POST.get("product_qty"))
            product_check = models.Product.objects.get(id=product_id)
            if product_check:
                if models.Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': "Item already in Cart"})
                else:
                    if product_check.quantity >= prod_qty:
                        models.Cart.objects.create(user=request.user, product_id=product_id, product_qty=prod_qty)
                        return JsonResponse({'status': "Product added to Cart"})
                    else:
                        return JsonResponse(
                            {'status': "Only " + str(product_check.quantity) + " of this product is available"})
            else:
                return JsonResponse({'status': "Something went wrong"})
        else:
            return JsonResponse({'status': "Login to continue"})


def update_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if models.Cart.objects.filter(user=request.user, product_id=prod_id):
            product_qty = int(request.POST.get('product_qty'))
            cart = models.Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = product_qty
            cart.save()
            return JsonResponse({'status': 'Item quantity updated'})
    return redirect('products')


def delete_cart_item(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if models.Cart.objects.filter(user=request.user, product_id=prod_id):
            print("true")
            cart_item = models.Cart.objects.filter(user=request.user, product_id=prod_id)
            cart_item.delete()
        return JsonResponse({'status': 'Item removed from cart'})
    return redirect('products')

