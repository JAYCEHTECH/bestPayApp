import requests
from django.shortcuts import render, redirect
from bestPayApp.forms import SendMessageForm


# Create your views here.
def home(request):
    form = SendMessageForm()
    if request.user.is_authenticated:
        form = SendMessageForm(
            initial={
                'name': request.user.username,
                'email': request.user.email
            }
        )
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            name = str(form.cleaned_data["name"])
            email = str(form.cleaned_data["email"])
            message = str(form.cleaned_data["message"])

            url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=UmpEc1JzeFV4cERKTWxUWktqZEs&to=0242442147&from=BP-Site&sms={name}\n{email}\n{message}"

            response = requests.request("GET", url)
            print(response.text)
            print(message)
    context = {'form': form}
    return render(request, 'layouts/index.html', context=context)


def services(request):
    return render(request, 'layouts/services.html')


def about(request):
    return render(request, 'layouts/about.html')


def blog(request):
    return render(request, 'layouts/blog-single.html')


def thank_you(request):
    return render(request, "layouts/thank_you.html")


def failed(request):
    return render(request, "layouts/failed.html")









