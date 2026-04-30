import os
import resend

def send_reset_email(to_email, reset_url):
    try:
        resend.api_key = os.environ["RESEND_API_KEY"]

        response = resend.Emails.send({
            "from": os.environ["DEFAULT_FROM_EMAIL"],
            "to": [to_email],  # ←ここ修正
            "subject": "パスワードリセット",
            "html": f"""
            <p>パスワードリセットはこちら👇</p>
            <a href="{reset_url}">{reset_url}</a>
            """
        })

        print("送信成功:", response)

    except Exception as e:
        print("送信エラー:", e)