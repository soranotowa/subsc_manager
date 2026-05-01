from django.db import models
from accounts.models import CustomUser
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.core.validators import MinValueValidator

class Category(models.Model):
    GROUP_CHOICES = [
        ('entertainment', 'エンタメ'),
        ('life', '生活'),
        ('insurance', '保険'),
        ('other', 'その他'),
    ]
    order = models.IntegerField(default=0)

    name = models.CharField(max_length=100)  # 動画 / 音楽 / 通信
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)

    def __str__(self):
        return f"{self.get_group_display()} - {self.name}"
    
    class Meta:
        ordering = ["order"]

class Service(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    plan = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.plan:
            return f"{self.name} ({self.plan})"
        return self.name

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
            return f"{self.service.name} - {self.price}円"
        return f"{self.custom_name} - {self.price}円"
    
