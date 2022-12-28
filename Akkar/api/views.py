from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Superuser
# Create your views here.
@api_view(["GET"])
def index(request):
    return Response("Hello, world. You're at the api index.")
@api_view(["POST"])
def ifadmin(request):
    #get the email from client request
    param=request.data["email"]
    print(param)
    try:
        instance=Superuser.objects.get(email=param)
    except:
        return Response("not found")
    #print()
    return Response("is admin")
    #print(instance)   