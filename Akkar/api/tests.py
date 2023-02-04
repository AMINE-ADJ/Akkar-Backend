from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from .models import Annonce , Utilisateur , Contact ,Localisation  , Image
from .views import postannonce

from django.urls import reverse

# Create your tests here.

class PostMessageTestCase(APITestCase) : 
        
    def test_post_message(self ) :
  
        # self.athenticate()
        message_data = {
                    "id": 1,
                    "offre": "we give  56000",
                    "telephone": "0656454854",
                    "nom": "fouad",
                    "email": "f.khalil@esi-sba.dz",
                    "date": "2023-01-12T17:38:24.396047+01:00",
                    "annonce":1
                }
        
        response = self.client.post('http://127.0.0.1:8000/api/sendmessage/' , message_data) 
        print(response.data , '------------')
        self.assertEqual(response.status_code, 201 )
        
        
class GetAllMessagesTestCase(APITestCase) : 
       
    def test_get_all_messages(self) :
        response =  self.client.get('http://127.0.0.1:8000/api/?id=ka_adjou@esi.dz')
        self.assertEqual(response.status_code, 200 )
        
    
class PostAnnonceTestCase(APITestCase):
    def setUp(self):
        # create user to use for the test
        self.user = Utilisateur.objects.create(email='test_user@example.com', username='test_user')
        self.request = APIRequestFactory()


    def test_post_annonce(self):
        # setup the data to be posted
        data = {
            'id': self.user.id,
            'categorie': 'category_test',
            'type': 'type_test',
            'surface': 'surface_test',
            'description': 'description_test',
            'prix': 'prix_test',
            'annonceuremail': 'annonceuremail_test',
            'nom': 'nom_test',
            'prenom': 'prenom_test',
            'email': 'email_test',
            'telephone': 'telephone_test',
            'adresseannonceur': 'adresseannonceur_test',
            'wilaya': 'wilaya_test',
            'commune': 'commune_test',
            'latitude': 'latitude_test',
            'longitude': 'longitude_test'
        }
        
        request = self.request.post('http://127.0.0.1:8000/api/postannonce/', data)
        response = postannonce(request)
        # make a post request to postannonce view
        # response = self.client.post()

        # assert the response status code is 201 created
        self.assertEqual(response.status_code, 201)

        # assert the response content is as expected
        self.assertEqual(response.data, 'votre annonce a été enregistrer')

        # assert the annonce, contact and localisation objects are created
        annonce = Annonce.objects.get(utilisateur=self.user)
        self.assertIsNotNone(annonce)
        self.assertEqual(annonce.titre, 'category_test type_test wilaya_test commune_test')
        self.assertEqual(annonce.categorie, 'category_test')
        self.assertEqual(annonce.type, 'type_test')
        self.assertEqual(annonce.surface, 'surface_test')
        self.assertEqual(annonce.description, 'description_test')
        self.assertEqual(annonce.prix, 'prix_test')
        self.assertEqual(annonce.annonceuremail, 'annonceuremail_test')
        
        contact = Contact.objects.get(annonce=annonce)
        self.assertIsNotNone(contact)
        self.assertEqual(contact.telephone, 'telephone_test')
        self.assertEqual(contact.email, 'email_test')
        
        localisation = Localisation.objects.get(annonce=annonce)
        self.assertIsNotNone(localisation)

    
