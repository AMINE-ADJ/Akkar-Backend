from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Utilisateur,Annonce,Contact,Localisation,Image
from .serializers import AnnonceSerializer,AnnonceDetailSerializer,UtilisateurSerializer , MessageSerializer , AnnanceMessagesSerializer
import requests
import time
from bs4 import BeautifulSoup
import datetime
# Create your views here.
@api_view(["GET"])
def index(request):
    return Response("Hello, world. You're at the api index.")
# @api_view(["DELETE"])
# def deleteall(request):
#     Annonce.objects.all().delete()
#     return Response("deleted")
#pour gerer les utilisateurs les utilisateurs 
@api_view(["POST"])
def utilisateurs(request):
    param=request.data["email"]
    try:
        instance=Utilisateur.objects.get(email=param)
        if instance:
            res=UtilisateurSerializer(instance).data
            return Response(res)
    except: 
        serializer=UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    
#pour voir toutes les annonces avant rechercher
@api_view(["GET"])
def afficherannonces(request,page):
    queryset=Annonce.objects.all()[(page-1)*40:page*40]
    res=AnnonceSerializer(queryset,many=True).data
    return Response(res)
    
#pour la recherche et le filtrage
@api_view(["POST"])
def filterannonce(request,page):
    #titre et description premiere recherche
    param=request.data['param']
    type=request.data['type']
    #recherche sans filtres, si le type n'existe pas dans le body de la requette
    queryset1=Annonce.objects.filter(titre__icontains=param)
    queryset2=Annonce.objects.filter(description__icontains=param)
    finalqueryset=queryset1 | queryset2
    #recherche avec filtres
    wilaya=request.data['wilaya']
    commune=request.data['commune']
    newestdate=request.data["newestdate"]
    oldestdate=request.data["oldestdate"]
    if not newestdate:
        finalqueryset=finalqueryset.filter(type__icontains=type
        ).filter(localisation__wilaya__icontains=wilaya
        ).filter(localisation__commune__icontains=commune)
        res={}
        res=AnnonceSerializer(finalqueryset[(page-1)*40:page*40],many=True).data
        return Response(res)
    else:
        finalqueryset=finalqueryset.filter(type__icontains=type
        ).filter(localisation__wilaya__icontains=wilaya
        ).filter(localisation__commune__icontains=commune).filter(date__lte=newestdate
        ).filter(date__gte=oldestdate)
        res={}
        res=AnnonceSerializer(finalqueryset[(page-1)*40:page*40],many=True).data
        return Response(res)
#detail annonce selon pk (id)
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
    identificateur=request.data["id"]
    titre=request.data["categorie"]+" "+request.data["type"]+" "+request.data["wilaya"]+" "+request.data["commune"]
    utilisateur=Utilisateur.objects.get(id=identificateur)
    annonce=Annonce.objects.create(utilisateur=utilisateur,titre=titre,
    categorie=request.data["categorie"],type=request.data["type"],
    surface=request.data["surface"],description=request.data["description"] or None,
    prix=request.data["prix"],annonceuremail=request.data["annonceuremail"])
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
    for value in values:
        if value.isnumeric() and values[value]:
            Image.objects.create(photo=values[value],annonce=annonce)
    return Response("votre annonce a été enregistrer")

#afficher mes annonces avec limite des resultats selon le nombre de la page
@api_view(["POST"])
def mesannonces(request,page):
    queryset=Annonce.objects.filter(utilisateur__id=request.data['id'])
    res=AnnonceSerializer(queryset[(page-1)*40:page*40], many=True).data
    return Response(res)

#supprimer annonce selon pk (id)
@api_view(['DELETE'])
def supprimerannonce(request,pk):
    Annonce.objects.get(id=pk).delete()
    return Response("votre annonce a été supprimer")

#webscraping du site annonce-algerie
@api_view(['POST'])
def lancerwebscraping(request):
    scrapingtime=int(request.data['scrapingtime'])
    scrapingtime=scrapingtime // 2
    pagecpt=1
    while pagecpt <= scrapingtime:
        if pagecpt==1:
            page=requests.get("http://www.annonce-algerie.com/AnnoncesImmobilier.asp").text
        else:
            page=requests.get(f"http://www.annonce-algerie.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=DZ&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num={pagecpt}").text
        time.sleep(5)
        soup=BeautifulSoup(page,'lxml')
        anchors=soup.find_all('a')
        #avoir touts les liens vers les annonces dans le tableau des immobiliers
        for anchor  in anchors :
            lien=anchor["href"]
            if "cod_ann" in lien:
                #print(lien)
                #print(20*'#')
                #scraping du lien de l'annonce
                pagedetail=requests.get(f"http://www.annonce-algerie.com/{lien}").text
                time.sleep(5)
                soupdetail=BeautifulSoup(pagedetail,'lxml')
                params=soupdetail.find_all('td',class_='da_field_text')
                #avoir les informations des annonces et les normaliser
                datalist=[]
                for param in params:
                    #print(param.text)
                    data=param.text
                    datalist.append(data.replace("\xa0","").replace("\r","").replace("\n","").replace("\t",""))
                    #print(20*"#")
                check=soupdetail.find(id='all_photos')
                if check:
                    divs=soupdetail.find(id='all_photos').find_all('a')
                    for anchor in divs:
                        img=anchor["href"].replace("javascript:photo_apercu('","")
                        #print(img)
                        datalist.append(img)
                soupcontact=BeautifulSoup(pagedetail,'lxml')
                contact=soupcontact.find("span",class_="da_contact_value")
                #print(contact.text)
                #list qui contient toutes les infomations
                datalist.append(contact.text)
                #print(datalist)   
                #fin de la recherche des informations
                #compteur pour avoir les informations de l'annonce
                cpt=0
                #categorie et type
                catettypeann=datalist[cpt][8:]
                categorie=catettypeann[:catettypeann.find(">")]
                #print(categorie)
                typeann=catettypeann[len(categorie)+1:]
                #print(typeann)
                cpt=cpt+1
                #wilaya et commune
                wilayacomm=datalist[cpt][9:]
                wilaya=wilayacomm[:wilayacomm.find(">")]
                #print(wilaya)
                commad=wilayacomm[len(wilaya)+1:]
                comm=commad[:commad.find(">")]
                #print(comm)
                cpt=cpt+1
                #surface
                if not datalist[cpt][:datalist[cpt].find("m")].replace(" ","").isnumeric():
                    cpt=cpt+1
                surface=datalist[cpt][:datalist[cpt].find("m")]
                #print(surface)
                cpt=cpt+1
                #prix
                prix=datalist[cpt][:datalist[cpt].find("D")]
                #print(prix)
                cpt=cpt+1
                #description
                description=datalist[cpt]
                #print(description)
                cpt=cpt+2
                #date
                date=datalist[cpt].replace("/","-")
                correctdate=datetime.datetime.strptime(date[6:]+"-"+date[3:5]+"-"+date[:2], '%Y-%m-%d').date()
                #print(correctdate)
                cpt=cpt+1
                imagelist=[]
                #les liens vers les photos 
                for item in datalist[cpt:]:
                    if "upload" in item:
                        imagelist.append(item[:item.find("'")])
                        cpt=cpt+1
                #num de telephone
                telephone=datalist[cpt]
                #print(telephone)
                #enregistrer l'annonce avant
                titre=categorie+" "+typeann+" "+wilaya+" "+comm
                instance=Utilisateur.objects.get(id=43)
                annonce=Annonce.objects.create(utilisateur= instance, titre=titre,
                categorie=categorie,type=typeann,
                surface=surface,description=description or None,
                prix=prix,annonceuremail="annonce-algerie",date=correctdate)
                
                #enregistrer le contact
                Contact.objects.create(annonce=annonce,telephone=telephone)
                #enregistrer la localisation
                Localisation.objects.create(annonce=annonce,wilaya=wilaya,
                commune=comm)
                #enregistrer les photos s'ils existent
                for value in imagelist:                
                        Image.objects.create(lien=value,annonce=annonce)
        pagecpt=pagecpt+1
    return Response("operation terminer")


#post message
@api_view(['POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
def send_message(request) : 
    serializer = MessageSerializer(data=request.data )
    if serializer.is_valid(raise_exception=True) :
        serializer.save()
        return Response({"status":"200"}) #the messsage is sent with success
    
#get messages
@api_view(["POST"])
def get_all_messages(request) : 
 
    id= request.data['id']
    queryset=Annonce.objects.filter(annonceuremail=id)
    #paginate
    paginator = PageNumberPagination()
    paginator.page_size = 5
    paginated_query_set =paginator.paginate_queryset(queryset, request)
    #serialiaze
    data = AnnanceMessagesSerializer(paginated_query_set , many=True).data
    print(data)
    return paginator.get_paginated_response(data)
