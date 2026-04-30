import os
import resend

def send_reset_email(to_email, reset_url):
    resend.api_key = os.environ["RESEND_API_KEY"]

    resend.Emails.send({
        "from": os.environ["DEFAULT_FROM_EMAIL"],
        "to": to_email,
        "subject": "パスワードリセット",
        "html": f"""
        <p>パスワードリセットはこちら👇</p>
        <a href="{reset_url}">{reset_url}</a>
        """
    })