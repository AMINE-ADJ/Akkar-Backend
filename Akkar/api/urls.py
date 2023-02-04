from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('utilisateurs/',views.utilisateurs,name='utilisateurs'),
    path('filterannonce/<int:page>',views.filterannonce,name='filterannonce'),
    path('detailannonce/<int:pk>',views.detailannonce,name='detailannonce'),
    path("postannonce/",views.postannonce,name="postannonce"),
    path("mesannonces/<int:page>",views.mesannonces,name="mesannonces"),
    path('supprimerannonce/<int:pk>',views.supprimerannonce,name="supprimerannonce"),
    path('lancerwebscraping/',views.lancerwebscraping,name="lancerwebscraping"),
    path("afficherannonces/<int:page>",views.afficherannonces,name="afficherannonces"),
    #path("deleteall/",views.deleteall,name="deleteall")
    
    path("sendmessage/",views.send_message,name="sendmessage"),
    path("messages/",views.get_all_messages,name="messages"),
    path("email/",views.get_annonce_with_email,name="email"),
    path("users/",views.get_users,name="users"),
]