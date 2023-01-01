from django.contrib import admin
from .models import SuperUser,Annonce,Image,Localisation,Contact
# Register your models here.
admin.site.register(SuperUser)
admin.site.register(Annonce)
admin.site.register(Image)
admin.site.register(Localisation)
admin.site.register(Contact)