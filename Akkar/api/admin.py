from django.contrib import admin
from .models import Annonce,Image,Localisation,Contact,Utilisateur
# Register your models here.
admin.site.register(Annonce)
admin.site.register(Image)
admin.site.register(Localisation)
admin.site.register(Contact)
admin.site.register(Utilisateur)