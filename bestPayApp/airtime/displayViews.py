from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect

from bestPayApp import helper


def display_name(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        name = helper.display_name(phone)

        return JsonResponse({'status': f"{name}"})
    return redirect('airtime')
