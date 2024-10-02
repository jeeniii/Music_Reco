from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 메인 페이지
    path('get_tracks/', views.get_tracks, name='get_tracks'), # 트랙 정보 불러오는 페이지
]