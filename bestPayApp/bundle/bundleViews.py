import json
from time import sleep

import requests
from decouple import config
from django.contrib import messages
from django.shortcuts import render, redirect
from bestPayApp.forms import VodafoneBundleForm, MTNBundleForm, AirtelTigoBundleForm
from bestPayApp import helper, models


def bundle(request):
    return render(request, 'layouts/services/bundle.html')


def mtn_all_bundles(request):
    return render(request, 'layouts/services/mtn-all-bundles.html')


def at_all_bundles(request):
    return render(request, 'layouts/services/at-all-bundles.html')


def vodafone(request):
    form = VodafoneBundleForm()
    if request.method == "POST":
        form = VodafoneBundleForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            offer_chosen = form.cleaned_data["offers"]

            voda_codes = helper.voda_codes
            value = f"\"{voda_codes[float(offer_chosen)]}\""
            amount = float(offer_chosen)
            amount_to_be_charged = helper.trim_amount(float(offer_chosen))
            client_ref = helper.ref_generator(2)
            provider = "Vodafone Bundle"
            return_url = f"http://127.0.0.1:8000/send_vodafone_bundle/{client_ref}/{phone_number}/{amount}/{value}"

            response = helper.execute_payment(amount_to_be_charged, client_ref,
                                              provider, return_url)
            print(response.json())
            data = response.json()

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                return redirect('failed')

    context = {'form': form}
    return render(request, 'layouts/services/voda-bundle.html', context=context)


def send_voda_bundle(request, client_ref, phone_number, amount, value):
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
                    f'http://127.0.0.1:8000/send_vodafone_bundle/{client_ref}/'
                    f'{phone_number}/{amount}/{value}')
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            reference = f"\"{client_ref}\""

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/33d27e7d-6dd5-4899-b702-6c9022bea8c7\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : " + value + "\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_voda_bundle_transaction = models.VodafoneBundleTransaction.objects.create(
                    user=current_user,
                    email=current_user.email,
                    bundle_number=phone_number,
                    offer=f"{amount}-{value}",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_voda_bundle_transaction.save()
                return redirect('thank_you')
            else:
                print(response.json())
                print("Not 200 error")
                new_voda_bundle_transaction = models.VodafoneBundleTransaction.objects.create(
                    user=current_user,
                    email=current_user.email,
                    bundle_number=phone_number,
                    offer=f"{amount}-{value}",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_voda_bundle_transaction.save()
                return redirect("failed")
        else:
            print("last error")
            return redirect('failed')


# ======================================= MTN BUNDLE =================================================

def mtn(request):
    form = MTNBundleForm()
    if request.method == "POST":
        form = MTNBundleForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            offer_chosen = form.cleaned_data["offers"]

            mtn_codes = helper.mtn_codes
            value = f"\"{mtn_codes[float(offer_chosen)]}\""
            print(value)
            amount = float(offer_chosen)
            amount_to_be_charged = helper.trim_amount(float(offer_chosen))
            client_ref = helper.ref_generator(2)
            provider = "MTN Bundle"
            return_url = f"http://127.0.0.1:8000/send_mtn_bundle/{client_ref}/{phone_number}/{amount}/{value}"

            response = helper.execute_payment(amount_to_be_charged, client_ref,
                                              provider, return_url)
            print(response.json())
            data = response.json()

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                return redirect('failed')

    context = {'form': form}
    return render(request, 'layouts/services/mtn-bundle.html', context=context)


def send_mtn_bundle(request, client_ref, phone_number, amount, value):
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
                    f'http://127.0.0.1:8000/send_mtn_bundle/{client_ref}/'
                    f'{phone_number}/{amount}/{value}')
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"
            reference = f"\"{client_ref}\""

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/33d27e7d-6dd5-4899-b702-6c9022bea8c7\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : " + value + "\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_bundle_transaction = models.MTNBundleTransaction.objects.create(
                    user=current_user,
                    email=current_user.email,
                    bundle_number=phone_number,
                    offer=f"{amount}-{value}",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_bundle_transaction.save()
                return redirect('thank_you')
            else:
                print(response.json())
                print("Not 200 error")
                new_mtn_bundle_transaction = models.MTNBundleTransaction.objects.create(
                    user=current_user,
                    email=current_user.email,
                    bundle_number=phone_number,
                    offer=f"{amount}-{value}",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_bundle_transaction.save()
                return redirect("failed")
        else:
            print("last error")
            return redirect('failed')


def airtel_tigo(request):
    form = AirtelTigoBundleForm()
    if request.method == "POST":
        form = AirtelTigoBundleForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            offer_chosen = form.cleaned_data["offers"]

            at_codes = helper.at_codes
            value = f"\"{at_codes[float(offer_chosen)]}\""
            print(value)
            amount = float(offer_chosen)
            amount_to_be_charged = helper.trim_amount(float(offer_chosen))
            client_ref = helper.ref_generator(2)
            provider = "AirtelTigo Big Time Bundle"

            return_url = f"http://127.0.0.1:8000/send_at_bundle/{client_ref}/{phone_number}/{amount}/{value}"

            response = helper.execute_payment(amount_to_be_charged, client_ref,
                                              provider, return_url)
            print(response.json())
            data = response.json()

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                return redirect('failed')

    context = {'form': form}
    return render(request, 'layouts/services/at-bundle.html', context=context)


def send_at_bundle(request, client_ref, phone_number, amount, value):
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
                    f'http://127.0.0.1:8000/send_at_bundle/{client_ref}/'
                    f'{phone_number}/{amount}/{value}')
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/06abd92da459428496967612463575ca"
            reference = f"\"{client_ref}\""

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/33d27e7d-6dd5-4899-b702-6c9022bea8c7\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : " + value + "\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                desc = helper.airtime_description(client_ref=client_ref)
                new_at_bundle_transaction = models.AirtelTigoBundleTransaction.objects.create(
                    user=current_user,
                    email=current_user.email,
                    bundle_number=phone_number,
                    offer=f"{amount}-{value}",
                    reference=client_ref,
                    transaction_status="Success",
                    description=desc
                )
                new_at_bundle_transaction.save()
                return redirect('thank_you')
            else:
                print(response.json())
                print("Not 200 error")
                new_at_bundle_transaction = models.AirtelTigoBundleTransaction.objects.create(
                    user=current_user,
                    email=current_user.email,
                    bundle_number=phone_number,
                    offer=f"{amount}-{value}",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_at_bundle_transaction.save()
                return redirect("failed")
        else:
            print("last error")
            return redirect('failed')
