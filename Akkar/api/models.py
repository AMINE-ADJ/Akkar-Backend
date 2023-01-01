from django.db import models
#admin model for admins table

class SuperUser(models.Model):
    email=models.CharField(max_length=255)
    def __str__(self):
        return self.email 

class Annonce(models.Model):
    titre=models.CharField(max_length=63,default='dafault')
    categorie=models.CharField(max_length=31,default='dafault')
    type=models.CharField(max_length=31,default='dafault')
    surface=models.CharField(max_length=15,default='dafault')
    description=models.TextField(null=True,blank=True)
    prix=models.CharField(max_length=31,default='dafault')
    annonceurid=models.CharField(max_length=31,default='dafault')
    date=models.DateField(auto_now_add=True)

class Image(models.Model):
    photo=models.ImageField(upload_to='pictures',blank=True,null=True)
    annonce=models.ForeignKey(Annonce, on_delete=models.CASCADE)

class Contact(models.Model):
    nom=models.CharField(max_length=31)
    prenom=models.CharField(max_length=31,null=True,blank=True)
    email=models.CharField(max_length=31,null=True,blank=True)
    adresseannonceur=models.CharField(max_length=31,null=True,blank=True)
    telephone=models.CharField(max_length=15)
    annonce=models.OneToOneField(Annonce,on_delete=models.CASCADE)

    
class Localisation(models.Model):
    wilaya=models.CharField(max_length=31)
    commune=models.CharField(max_length=31)
    latitude=models.CharField(max_length=31)
    longitude=models.CharField(max_length=31)
    annonce=models.OneToOneField(Annonce,on_delete=models.CASCADE)



# Create your models here.
