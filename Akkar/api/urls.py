from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/',views.ifadmin,name='ifadmin'),
    path('filterannonce/',views.filterannonce,name='filterannonce')
]