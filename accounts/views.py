from django.shortcuts import render, redirect

import os

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from .mail import send_reset_email


# def test_email(request): テスト用
#     try:
#         resend.api_key = os.environ["RESEND_API_KEY"]

#         resend.Emails.send({
#             "from": "onboarding@resend.dev",
#             "to": "t.soooora@gmail.com",  # ←ここ自分のに
#             "subject": "テスト",
#             "html": "<p>メール成功！</p>"
#         })

#         return HttpResponse("送信OK")

#     except Exception as e:
#         return HttpResponse(f"エラー: {e}")

def custom_password_reset(request):
    print("🔥 custom_password_reset 呼ばれた") 

    if request.method == "POST":
        print("📩 POST来た") 
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            users = list(form.get_users(form.cleaned_data["email"]))
            print("👤 users:", users)

            for user in users:
                print("📧 送信対象:", user.email)

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                domain = get_current_site(request).domain
                reset_url = f"https://{domain}" + reverse(
                    "account_reset_password_from_key",
                    kwargs={"uidb36": uid, "key": token} 
                )

                send_reset_email(user.email, reset_url)

            return redirect("/accounts/password/reset/done/")
    else:
        form = PasswordResetForm()

    return render(request, "account/password_reset.html", {"form": form})