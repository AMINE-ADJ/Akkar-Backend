from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Annonce , Utilisateur

from django.urls import reverse

# Create your tests here.

class PostMessageTestCase(APITestCase) : 
    
    
    # def test_get_all_messages(self) :
        
    #     response =  self.client.get('http://127.0.0.1:8000/api/messages/?id=ka_beraoud@esi.dz')
    #     self.assertEqual(response.status_code, 200 )


    
    # def test_post_message(self ) :
  
    #     # self.athenticate()
    #     message_data = {
    #                 "id": 1,
    #                 "offre": "we give  56000",
    #                 "telephone": "0656454854",
    #                 "nom": "fouad",
    #                 "email": "f.khalil@esi-sba.dz",
    #                 "date": "2023-01-12T17:38:24.396047+01:00",
    #                 "annonce":1
    #             }
    #     response = self.client.post('http://127.0.0.1:8000/api/sendmessage/' , message_data) 
    #     print(response.data , '------------')
    #     self.assertEqual(response.status_code, 201 )
        
    pass
    
