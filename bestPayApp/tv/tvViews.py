import json

import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect

from bestPayApp import helper, models
from bestPayApp.forms import TvForm, TVCheckForm


def tv_all(request):
    return render(request, "layouts/services/tv-all.html")


def tv_check(request):
    form = TVCheckForm()
    context = {'form': form}
    return render(request, "layouts/services/tv-check.html", context=context)


def balance_check(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        provider = request.POST.get('provider')

        data = helper.get_balance(account_number, provider)
        name = data["Data"][0]["Value"]
        account_balance = data["Data"][0]["Amount"]
        amount_due = data["Data"][1]["Value"]

        return JsonResponse({'status': f"Account Name: {name} <br> Amount Due: {amount_due}"})

    return redirect('tv_check')


def tv(request):
    form = TvForm()
    if request.method == "POST":
        form = TvForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data["account_number"]
            amount = form.cleaned_data["amount"]
            tv_provider = form.cleaned_data["provider"]

            amount = float(amount)
            amount_to_be_charged = helper.trim_amount(float(amount))
            client_ref = helper.ref_generator(2)
            provider = f"TV Subscription - {tv_provider}"

            return_url = f"http://127.0.0.1:8000/add_amount_to_tv_account/" \
                         f"{client_ref}/{account_number}/{amount}/{tv_provider}"

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
    return render(request, "layouts/services/tv.html", context=context)


def add_amount_to_tv_account(request, client_ref, account_number, amount, tv_provider):
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
                    f'http://127.0.0.1:8000/add_amount_to_tv_account/{client_ref}/'
                    f'{account_number}/{amount}/{tv_provider}')
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = helper.tv_provider_url(provider=tv_provider)
            reference = f"\"{client_ref}\""

            payload = "{\r\n    \"Destination\": " + account_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/1a65f655-2cb2-4693-a406-408a9467d45e\",\r\n    \"ClientReference\": " + reference + "\r\n}"

            headers = {
                'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                desc = helper.airtime_description(client_ref=client_ref)
                new_tv_transaction = models.TvTransaction.objects.create(
                    user=current_user,
                    email=current_user.email,
                    account_number=account_number,
                    amount=amount,
                    reference=client_ref,
                    transaction_status="Success",
                    description=desc
                )
                new_tv_transaction.save()
                return redirect('thank_you')
            else:
                print(response.json())
                print("Not 200 error")
                new_tv_transaction = models.AirtelTigoBundleTransaction.objects.create(
                    user=current_user,
                    email=current_user.email,
                    account_number=account_number,
                    amount=amount,
                    reference=client_ref,
                    transaction_status="Failed",
                )
                new_tv_transaction.save()
                return redirect("failed")
        else:
            print("last error")
            return redirect('failed')

