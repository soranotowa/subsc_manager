from django.db import models
from accounts.models import CustomUser
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.core.validators import MinValueValidator

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('video', '動画'),
        ('music', '音楽'),
        ('other', 'その他エンタメ系'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    plan = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.service:
            return str(self.service)
        return self.custom_name

class Subscription(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField("料金（ユーザー設定）")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    custom_name = models.CharField("サービス名（手入力）", max_length=255, blank=True)

    CURRENCY_CHOICES = [
        ('JPY', '円'),
        ('USD', 'ドル'),
        ('EUR', 'ユーロ'),
    ]

    currency = models.CharField(
        "通貨",
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='JPY'
    )

    start_date = models.DateField("開始日")
    memo = models.TextField("メモ", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    INTERVAL_UNIT_CHOICES = [
        ('month', 'ヶ月'),
        ('year', '年'),
    ]

    interval_value = models.IntegerField("更新間隔",validators=[MinValueValidator(1)])
    interval_unit = models.CharField(
        "単位",
        max_length=10,
        choices=INTERVAL_UNIT_CHOICES,
        default='month'
    )

    def next_renewal_date(self):
        today = timezone.now().date()
        next_date = self.start_date

        while next_date < today:
            if self.interval_unit == 'month':
                next_date += relativedelta(months=self.interval_value)
            elif self.interval_unit == 'year':
                next_date += relativedelta(years=self.interval_value)

        return next_date

    def days_until_renewal(self):
        today = timezone.now().date()
        next_date = self.next_renewal_date()

        diff = (next_date - today).days

        if diff > 0:
            return f"次回更新まであと{diff}日"
        elif diff == 0:
            return "今日"
        else:
            return f"{abs(diff)}日経過"

    def is_soon(self):
        today = timezone.now().date()
        next_date = self.next_renewal_date()
        diff = (next_date - today).days

        if self.interval_unit == 'month':
            return diff <= 7
        elif self.interval_unit == 'year':
            return diff <= 30
        return False

    def __str__(self):
        if self.service:
            return self.service.name
        return self.custom_name
    
