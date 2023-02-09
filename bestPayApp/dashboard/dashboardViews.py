from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bestPayApp import models, helper


@login_required(login_url='login')
def dashboard(request):
    airtime_transactions = models.AirtimeTransaction.objects.filter(user=request.user).order_by('transaction_date').reverse()
    context = {'airtime_txns': airtime_transactions}
    return render(request, 'dashboard/layouts/index.html', context=context)


@login_required(login_url='login')
def txn_table(request, keyword):
    data = helper.data_needed_from_model(keyword, request.user)
    model_data = data["model_data"]
    heading = data["heading"]
    return render(request, 'dashboard/layouts/tables.html', context={'data': model_data, 'heading':heading})
