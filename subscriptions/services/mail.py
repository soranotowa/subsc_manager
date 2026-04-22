from django.core.mail import send_mail
from django.conf import settings

def send_renewal_mail(user, subscriptions):
    subject = "【サブスク管理】更新間近のお知らせ"

    message = "以下のサブスクが更新間近です：\n\n"

    for sub in subscriptions:
        name = sub.service.name if sub.service else sub.custom_name
        message += f"- {name}（{sub.days_until_renewal}）\n"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )