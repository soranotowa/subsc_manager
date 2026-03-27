from django.urls import path
from .import views

app_name = 'diary'
urlpatterns = [
    path('',views.IndexView.as_view(), name="index"),
    path('inquiry/',views.InquiryView.as_view(),name="inquiry"),
    # 「https://<ホスト名>/diary-list/」というURLでアクセスがあった場合にはDiaryListViewというビューに処理をさせる
    path('diary-list/',views.DiaryListView.as_view(),name="diary_list"),
    path('diary-detail/<int:pk>/', views.DiaryDetailView.as_view(), name="diary_detail"),
    # diary_createというURLでアクセスがあるとDiaryCreateViewビューに処理を移譲
    path('diary-create/',views.DiaryCreateView.as_view(),name="diary_create"),
    # 既存の日記の編集
    path('diary-update/<int:pk>/',views.DiaryUpdateView.as_view(),name="diary_update"),
    # 既存の日記の削除
    path('diary-delete/<int:pk>/',views.DiaryDeleteView.as_view(),name="diary_delete"),
]