import email
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from acc_users.models import CustomUser

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
User = get_user_model()


class UserListListViewTest(TestCase):
    user = ""

    @classmethod
    def setUpTestData(self):
        user = User.objects.create(username='admin', email='admin@gmail.com', first_name='firstname', last_name='lastname', phonenumber='09030303030')     
        user.is_superuser = True
        user.is_staff = True
        user.set_password("123")
        user.save()
        self.user = user
  

    def test_refresh_token(self):
        url = "/token/refresh/"
        user = self.user
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh)}
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, 200)

    def test_verify_token(self):
        url = "/token/verify/"
        user = self.user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        data = {"token": str(access)}
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        client = APIClient()
        url = f"/accountapi/login/"
        data = {
            "username": "admin",
            "password": "123",          
        }
        response = client.post(url, data=data)     
        self.assertEqual(response.status_code, 201)

    def test_user_can_login(self):
        client = APIClient()
        url = f"/accountapi/createuser/"
        data = {
            "username": "username",
            "email": "email@gmail.com",
            "password": "123",   
            "phonenumber":"phonenumber",
            "first_name":"first_name",
            "last_name":"last_name"              
        }
        response = client.post(url, data=data)       
        self.assertEqual(response.status_code, 201)
 