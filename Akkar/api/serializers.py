from rest_framework import serializers
from api.models import Utilisateur,Annonce , Message

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model=Utilisateur
        fields= "__all__"

class AnnonceDetailSerializer(serializers.ModelSerializer):
    my_image=serializers.SerializerMethodField(read_only=True)
    my_localisation=serializers.SerializerMethodField(read_only=True)
    my_contact=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Annonce
        fields=["id","titre","categorie","type"
        ,"surface","description","annonceuremail"
        ,"prix","date","my_image","my_contact","my_localisation"]

    def get_my_image(self,obj):
        result=obj.image_set.all()
        listimage=[]
        if result:
            for pic in result:
                if pic.photo:
                    listimage.append("http://127.0.0.1:8000"+pic.photo.url)
                if pic.lien:
                    listimage.append("http://www.annonce-algerie.com"+pic.lien)
        return listimage

    def get_my_localisation(self,obj):
        result=obj.localisation
        return {
            "wilaya":result.wilaya,
            "commune":result.commune,
            "latitude":result.latitude,
            "longitude":result.longitude,
        }
    def get_my_contact(self,obj):
        result=obj.contact
        return{
            "nom":result.nom,
            "prenom":result.prenom,
            "email":result.email,
            "adresseannonceur":result.adresseannonceur,
            "telephone":result.telephone
        }

class AnnonceSerializer(serializers.ModelSerializer):
    my_image=serializers.SerializerMethodField(read_only=True)
    my_localisation=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Annonce
        fields=["id","titre","surface","prix",
        "date","annonceuremail","my_image","my_localisation"]

    def get_my_image(self,obj):
        result=obj.image_set.first()
        if result:
            if result.photo: 
                return "http://127.0.0.1:8000"+result.photo.url
            if result.lien:
                return "http://www.annonce-algerie.com"+result.lien


    def get_my_localisation(self,obj):
        result=obj.localisation
        return result.wilaya
    
    
class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Message
        fields= "__all__"
        
class AnnanceMessagesSerializer(serializers.ModelSerializer):
    message_set = MessageSerializer( read_only=True ,many=True )
    
    class Meta:
        model=Annonce
        fields= ["id","titre" , "message_set"] 
    
    class Meta : 
        ordering =  ['-date']