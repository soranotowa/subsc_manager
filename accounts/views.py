from django.shortcuts import render, redirect

import os

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import user_pk_to_url_str

from .mail import send_reset_email


def custom_password_reset(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            form.save(request=request)  # ← これが全部やる
            return redirect("/accounts/password/reset/done/")
    else:
        form = ResetPasswordForm()

    return render(request, "account/password_reset.html", {"form": form})

def create_superuser(request):
    User = get_user_model()

    if not User.objects.filter(email="test@example.com").exists():
        User.objects.create_superuser(
            username="admin",
            email="test@example.com",
            password="1221"
        )
        return HttpResponse("superuser created!")
    
    return HttpResponse("already exists")