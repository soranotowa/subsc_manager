from django.contrib import admin
from .models import CustomUser

# Register your models here.
# カスタムユーザモデルを管理サイトに登録
admin.site.register(CustomUser)