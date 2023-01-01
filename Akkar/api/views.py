from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SuperUser,Annonce
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
    param=request.data['param']
    #description=request.data['description']
    try:
        type=request.data['type']
    except:
        type=None
    if type==None:
        queryset1=Annonce.objects.filter(titre__icontains=param)
        queryset2=Annonce.objects.filter(description__icontains=param)
        finalqueryset=queryset1 | queryset2
        res={}
        print(1)
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
        res={}
        print("2")
        res=AnnonceSerializer(finalqueryset,many=True).data
        return Response(res)