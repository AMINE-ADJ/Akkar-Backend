from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SuperUser,Annonce,Contact,Localisation,Image
from .serializers import AnnonceSerializer,AnnonceDetailSerializer
# Create your views here.
@api_view(["GET"])
def index(request):
    return Response("Hello, world. You're at the api index.")
#api for checking if the user is admin
@api_view(["POST"])
def ifadmin(request):
    #get the email from client request
    param=request.data["email"]
    try:
        instance=SuperUser.objects.get(email=param)
    except:
        return Response("not admin")
    return Response("is admin")
#api for searching
@api_view(["POST"])
def filterannonce(request):
    #titre et description premier recherche
    print(request.data)
    param=request.data['param']
    #description=request.data['description']
    try:
        type= request.data['type']
    except:
        type=None
    if type==None:
        queryset1=Annonce.objects.filter(titre__icontains=param)
        queryset2=Annonce.objects.filter(description__icontains=param)
        finalqueryset=queryset1 | queryset2
        print(1)
        res={}
        res=AnnonceSerializer(finalqueryset,many=True).data
        return Response(res)
    else:
        #recherche avec filtres
        wilaya=request.data['wilaya']
        commune=request.data['commune']
        newestdate=request.data["newestdate"]
        oldestdate=request.data["oldestdate"]
        if not newestdate:
            queryset1=Annonce.objects.filter(titre__icontains=param)
            queryset2=Annonce.objects.filter(description__icontains=param)
            finalqueryset=queryset1 | queryset2
            finalqueryset=finalqueryset.filter(type__icontains=type
            ).filter(localisation__wilaya__icontains=wilaya
            ).filter(localisation__commune__icontains=commune)
        else:
            queryset1=Annonce.objects.filter(titre__icontains=param)
            queryset2=Annonce.objects.filter(description__icontains=param)
            finalqueryset=queryset1 | queryset2

            finalqueryset=finalqueryset.filter(type__icontains=type
            ).filter(localisation__wilaya__icontains=wilaya
            ).filter(localisation__commune__icontains=commune
            ).filter(date__lte=newestdate).filter(date__gte=oldestdate)

        # .filter(
        # date__lte=newestdate).filter(date__gte=oldestdate)
        print(2)
        res={}
        res=AnnonceSerializer(finalqueryset,many=True).data
        return Response(res)

@api_view(['GET'])
def detailannonce(request,pk):
    try:
        instance=Annonce.objects.get(id=pk)
        res=AnnonceDetailSerializer(instance).data
    except:
        return Response("not found")

    return Response(res)
#ajouter annonce
@api_view(['POST'])
def postannonce(request):
    #enregistrer l'annonce avant
    annonce=Annonce.objects.create(titre=request.data["titre"],
    categorie=request.data["categorie"],type=request.data["type"],
    surface=request.data["surface"],description=request.data["description"] or None,
    prix=request.data["prix"],annonceurid=request.data["annonceurid"])
    #enregistrer le contact
    Contact.objects.create(annonce=annonce,nom=request.data["nom"],
    prenom=request.data["prenom"] or None,email=request.data["email"] or None,
    telephone=request.data["telephone"],adresseannonceur=request.data["adresseannonceur"] or None)
    values=request.data
    #enregistrer la localisation
    Localisation.objects.create(annonce=annonce,wilaya=request.data["wilaya"],
    commune=request.data["commune"],latitude=request.data["latitude"],
    longitude=request.data["longitude"])
    #enregistrer les photos s'ils existent
    values=request.data
    print(values)
    for value in values:
        if value.isnumeric() and values[value]:
            Image.objects.create(photo=values[value],annonce=annonce)
    return Response("votre annonce a été enregistrer!")

#afficher mes annonces
@api_view(["POST"])
def mesannonces(request):
    queryset=Annonce.objects.filter(annonceurid=request.data["param"])
    res=AnnonceSerializer(queryset, many=True).data
    return Response(res)

#supprimer annonce
@api_view(['DELETE'])
def supprimerannonce(request,pk):
    Annonce.objects.get(id=pk).delete()
    return Response("votre annonce a été bien supprimer")
