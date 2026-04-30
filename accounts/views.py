from django.shortcuts import render

import os
import resend
from django.http import HttpResponse

def test_email(request):
    try:
        resend.api_key = os.environ["RESEND_API_KEY"]

        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "t.soooora@gmail.com",  # ←ここ自分のに
            "subject": "テスト",
            "html": "<p>メール成功！</p>"
        })

        return HttpResponse("送信OK")

    except Exception as e:
        return HttpResponse(f"エラー: {e}")
