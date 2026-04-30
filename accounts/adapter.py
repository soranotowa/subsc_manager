import os
import resend
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        resend.api_key = os.environ["RESEND_API_KEY"]

        # 件名（適当にカスタムOK）
        subject = "パスワードリセット"

        # 本文（シンプルでOK）
        reset_url = context.get("password_reset_url")

        html = f"""
        <p>パスワードリセットはこちら👇</p>
        <a href="{reset_url}">{reset_url}</a>
        """

        resend.Emails.send({
            "from": os.environ["DEFAULT_FROM_EMAIL"],
            "to": email,
            "subject": subject,
            "html": html
        })