from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from bestPayApp.forms import CustomUserForm
from django.shortcuts import render, redirect
from django.contrib import messages

from bestPayApp.models import CustomUser


def sign_up(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sign Up Successful. Log in to continue.")
            return redirect('login')
    context = {'form': form}
    return render(request, 'auth/signup.html', context=context)


def login_page(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('pass')

            user = authenticate(request, username=name, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Log in Successful')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
    return render(request, "auth/login.html")


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, "Log out successful")
    return redirect('home')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "passwords/password_reset_email.txt"
                    c = {
                        "name": user.first_name,
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'BestPay',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="passwords/password_reset.html",
                  context={"password_reset_form": password_reset_form})

