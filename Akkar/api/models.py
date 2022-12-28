from django.db import models
#admin model for admins table

class Superuser(models.Model):
    email=models.CharField(max_length=255)
    def __str__(self):
        return self.email 

    

# Create your models here.
