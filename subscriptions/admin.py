from django.contrib import admin
from .models import Service, Subscription, Category

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_filter = ("category__group", "category")
    ordering = ("category", "name")
    list_filter = ("category__group", "category")  # ← グループでも絞れる
    search_fields = ("name", "plan")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "price", "start_date", "interval_value", "interval_unit")
    list_filter = ("currency", "interval_unit")
    search_fields = ("service__name", "custom_name")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "order")
    list_filter = ("group",)
    ordering = ("order",)