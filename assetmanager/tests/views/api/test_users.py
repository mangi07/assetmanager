# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from jsonschema import validate

from ....models.user_models import UserType
from ....models.user_models import ExtendedUser
from django.contrib.auth.models import User


# TODO: test that all routes that should be protected return 403 for non-authenticated requests
# TODO: only superadmin can create manager and only manager can create regular user

class CreateUserTest(TestCase):
    """Test API for creating users."""
    def setUp(self):
        pass

    
    def test_create_user(self):
        """Superuser can successfully create manager user."""
        client = APIClient()
        superuser = User.objects.create_superuser(username='admin',
                                         email='',
                                         password='password')
        response = client.post(
            reverse('token-obtain-pair'),
            json.dumps({"username": "admin", "password": "password"}),
            content_type="application/json"
        )
        token = json.loads(response.content)['access']
        
        USERNAME = "manager user"
        # TODO: confirm password not validating - passes but it shouldn't
        payload = {
            "username": "manager user", "password": "password", "confirmPassword": "password",
            "department": "AV", "user_type": UserType.MANAGER.val
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
        #client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.post(
                reverse('create-user'),
                json.dumps(payload),
                content_type="application/json"
        )
        print("DEBUG: GOT HERE")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # query database to see if the user is really there
        user = User.objects.get(username = USERNAME)
        self.assertIsNotNone(user)
        
        manager_user = ExtendedUser.objects.first()
        self.assertEqual(manager_user.user.username, USERNAME)
        self.assertEqual(manager_user.department, "AV")
        self.assertEqual(manager_user.user_type, UserType.MANAGER.val)


    def test_user_cannot_create_manageruser(self):
        """Regular user cannot create manager user."""
        # create the regular user
        user = User.objects.create_user(username='regular user',
                                         email='',
                                         password='password')
        regular_user = ExtendedUser.objects.create(user=user,
                                        department="AV",
                                        user_type=UserType.REGULAR.val)
        
        # obtain access token
        client = APIClient()
        response = self.client.post(
            reverse('token-obtain-pair'),
            json.dumps(
                {"username": "regular user", "password": "password"}
            ),
            content_type="application/json"
        )
        token = json.loads(response.content)['access']
        
        # attempt to create manager admin
        payload = {
            "username": "manager user", "password": "123", "confirmPassword": "123",
            "department": "AV", "user_type": UserType.MANAGER.val
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response2 = client.post(
                reverse('create-user'),
                json.dumps(payload),
                content_type="application/json"
        )
        
        # assertions
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        # assert that a new user was not created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(ExtendedUser.objects.count(), 1)
        
        
class LoginUserTest(TestCase):
    """Test API login with JWT token authentication."""
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(username='admin',
                                         email='',
                                         password='password')
        
        self.response = self.client.post(
            reverse('token-obtain-pair'),
            json.dumps(
                {"username": "admin", "password": "password"}
            ),
            content_type="application/json"
        )
        
        
    def test_user_obtain_token(self):
        """Test username and password can obtain JWT token and refresh from API"""
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        token_dict = json.loads(self.response.content)
        self.assertTrue('access' in token_dict)
        self.assertTrue('refresh' in token_dict)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token_dict['access']))
        response = self.client.get(
            reverse('location-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    # TODO: test user can log in with obtained token
    
# TODO: test user can log out and blacklist token on server