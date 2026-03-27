from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 2026-02-28追加 CustomUserモデルクラスを定義
class CustomUser(AbstractUser):
    """拡張ユーザモデル"""

    class Meta:
        verbose_name_plural = 'CustomUser'
