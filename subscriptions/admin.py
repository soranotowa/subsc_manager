from django.contrib import admin
from .models import Service, Subscription, Category

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "plan", "price")
    list_filter = ("category",)
    search_fields = ("name", "plan")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "price", "start_date")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)