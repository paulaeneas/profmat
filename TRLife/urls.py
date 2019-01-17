from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:se_short_name>/', views.detail_substation, name='detail_substation'),
    path('<str:se_short_name>/<str:tr_name>', views.detail_transformer, name='detail_transformer'),
]
