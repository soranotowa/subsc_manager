from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.SubscriptionListView.as_view(), name='subscription_list'),
    path('detail/<int:pk>/', views.SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('create/', views.SubscriptionCreateView.as_view(), name='subscription_create'),
    path('update/<int:pk>/', views.SubscriptionUpdateView.as_view(), name='subscription_update'),
    path('delete/<int:pk>/', views.SubscriptionDeleteView.as_view(), name='subscription_delete'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('soon/', views.SoonSubscriptionListView.as_view(), name='subscription_soon'),
     path('create-admin/', views.create_admin),
]