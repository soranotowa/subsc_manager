from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 2026-02-28追加 CustomUserモデルクラスを定義
class CustomUser(AbstractUser):
    """拡張ユーザモデル"""

    display_name = models.CharField(
        "表示名",
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = 'CustomUser'