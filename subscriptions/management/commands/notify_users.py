from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from subscriptions.models import Subscription
from subscriptions.services.mail import send_renewal_mail

User = get_user_model()


class Command(BaseCommand):
    help = "更新間近のユーザーにメール送信"

    def handle(self, *args, **options):
        users = User.objects.all()

        sent_count = 0

        for user in users:
            subs = Subscription.objects.filter(user=user)
            soon = [s for s in subs if s.is_soon()]

            if soon:
                send_renewal_mail(user, soon)
                sent_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{sent_count}人にメール送信しました")
        )