from django.db import models
from datetime import date
#admin model for admins table

class Utilisateur(models.Model):
    email=models.CharField(max_length=255,default="ka_beraoud@esi.dz")
    isadmin=models.BooleanField(default=False)
    username=models.CharField(max_length=63,default="user")

    def __str__(self):
        return self.email 

class Annonce(models.Model):
    titre=models.CharField(max_length=63,default='dafault')
    categorie=models.CharField(max_length=31,default='dafault')
    type=models.CharField(max_length=31,default='dafault')
    surface=models.CharField(max_length=15,default='dafault')
    description=models.TextField(null=True,blank=True)
    prix=models.CharField(max_length=31,default='dafault')
    annonceuremail=models.CharField(max_length=31,null=True,blank=True,default="default")
    date=models.DateField(default=date.today)
    utilisateur=models.ForeignKey(Utilisateur,on_delete=models.CASCADE,default=3)
    class Meta:
        ordering=['-date']

class Image(models.Model):
    photo=models.ImageField(upload_to='pictures',blank=True,null=True)
    annonce=models.ForeignKey(Annonce, on_delete=models.CASCADE)
    lien=models.CharField(max_length=255,null=True,blank=True)

class Contact(models.Model):
    nom=models.CharField(max_length=31,null=True,blank=True)
    prenom=models.CharField(max_length=31,null=True,blank=True)
    email=models.CharField(max_length=31,null=True,blank=True)
    adresseannonceur=models.CharField(max_length=31,null=True,blank=True)
    telephone=models.CharField(max_length=15,null=True,blank=True)
    annonce=models.OneToOneField(Annonce,on_delete=models.CASCADE)

    
class Localisation(models.Model):
    wilaya=models.CharField(max_length=31)
    commune=models.CharField(max_length=31)
    latitude=models.CharField(max_length=31,null=True,blank=True)
    longitude=models.CharField(max_length=31,null=True,blank=True)
    annonce=models.OneToOneField(Annonce,on_delete=models.CASCADE)



# Create your models here.
