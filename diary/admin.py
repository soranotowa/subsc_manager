
from django.contrib import admin
from .models import Diary

# Register your models here.

# 管理サイトに日記モデルを登録
admin.site.register(Diary)