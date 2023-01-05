from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/',views.ifadmin,name='ifadmin'),
    path('filterannonce/',views.filterannonce,name='filterannonce'),
    path('detailannonce/<int:pk>',views.detailannonce,name='detailannonce'),
    path("postannonce/",views.postannonce,name="postannonce"),
    path("mesannonces/",views.mesannonces,name="mesannonces"),
    path('supprimerannonce/<int:pk>',views.supprimerannonce,name="supprimerannonce"),
    path('lancerwebscraping/',views.lancerwebscraping,name="lancerwebscraping")
]