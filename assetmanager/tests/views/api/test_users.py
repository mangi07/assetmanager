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

from .... import permissions

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


# TODO: test that all routes that should be protected return 403 for non-authenticated requests - maybe put this in middleware
# TODO: only superadmin can create manager and only manager can create regular user

class CreateUserTest(TestCase):
    """Test API for creating users."""

    ###########################################################################
    ### helper functions
    def create_user(self, user_type, username, password, department):
        """Creates user with user_type
        
        Args:
            user_type (:obj:`UserType`): An enum representing the type of user to be created.
            username (str): User's username.
            password (str): User's password.
            department (str): User's department.
        """
        user = None
        if user_type == UserType.SUPER:
            user = User.objects.create_superuser(username=username,
                                         email='',
                                         password=password)
        else:
            user = User.objects.create_user(username=username,
                                             email='',
                                             password=password)
        extended_user = ExtendedUser.objects.create(user=user,
                                        department=department,
                                        user_type=user_type.val)
                                        
        permissions.set_permissions_group(user, user_type.val)


    def create_user_token(self, client, user_type, department):
        """Creates user with user_type and returns token for that user's subsequent requests
        
        Args:
            client (:obj:`APIClient`): The APIClient object used to make requests.
            user_type (:obj:`UserType`): An enum representing the type of user to be created.

        Returns:
            str: token
        """
        username = 'user'
        password = 'password'
        
        user = self.create_user(user_type, username, password, department)
        response = client.post(
            reverse('token-obtain-pair'),
            json.dumps(
                {"username": username, "password": password}
            ),
            content_type="application/json"
        )
        token = json.loads(response.content)['access']
        
        return token
        
    
    def request_user_creation(self, client, user_type, username, token):
        """Creates user with user_type via another user's token-authenticated request
        
        Args:
            client (:obj:`APIClient`): The APIClient object used to make requests.
            user_type (:obj:`UserType`): An enum representing the type of user to be created.
            username (str): User name of user to be created.
            token (str): Token used to authenticate request.

        Returns:
            response (:obj:`rest_framework.response.Response`): response indicating success or failure
        """
        payload = {
            "username": username, "password": "password", "confirmPassword": "password",
            "department": "DEFAULT", "user_type": user_type.val
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))

        response = client.post(
                reverse('create-user'),
                json.dumps(payload),
                content_type="application/json"
        )
        return response

    
    ###########################################################################
    ### superuser can create manager and regular user
    def test_superuser_can_create_manager_user(self):
        """Superuser can successfully create manager user."""
        # set up superuser
        client = APIClient()
        superuser_department = "DEFAULT"
        token = self.create_user_token(client, UserType.SUPER, superuser_department)
        
        # request manager creation
        manager_username = "manageruser"
        response = self.request_user_creation(client, UserType.MANAGER, manager_username, token)
        
        # examine created manager user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # query database to see if the user is really there
        user = User.objects.get(username = manager_username)
        self.assertIsNotNone(user)
        manager_user = ExtendedUser.objects.get(user=user)
        self.assertEqual(manager_user.user.username, manager_username)
        self.assertEqual(manager_user.user_type, UserType.MANAGER.val)

    
    def test_superuser_can_create_regular_user(self):
        """Superuser can successfully create regular user."""
        # set up superuser
        client = APIClient()
        superuser_department = "DEFAULT"
        token = self.create_user_token(client, UserType.SUPER, superuser_department)
        
        # request regular user creation
        regular_username = "regularuser"
        response = self.request_user_creation(client, UserType.REGULAR, regular_username, token)
        
        # examine created regular user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # query database to see if the user is really there
        user = User.objects.get(username = regular_username)
        self.assertIsNotNone(user)
        regular_user = ExtendedUser.objects.get(user=user)
        self.assertEqual(regular_user.user.username, regular_username)
        self.assertEqual(regular_user.user_type, UserType.REGULAR.val)

    
    ###########################################################################
    ### manager cannot create superuser but can create regular user
    def test_manager_cannot_create_superuser(self):
        """Manager user cannot create superuser."""
        client = APIClient()
        token = self.create_user_token(client, UserType.MANAGER, "DEFAULT")
        super_username = "superuser"
        response = self.request_user_creation(client, UserType.SUPER, super_username, token)
        
        # assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # assert that a new user was not created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(ExtendedUser.objects.count(), 1)

    
    def test_manager_can_create_regular_user(self):
        """Manager can successfully create regular user."""
        # set up superuser
        client = APIClient()
        manager_department = "DEFAULT"
        token = self.create_user_token(client, UserType.MANAGER, manager_department)
        
        # request regular user creation
        regular_username = "regularuser"
        response = self.request_user_creation(client, UserType.REGULAR, regular_username, token)
        
        # examine created regular user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # query database to see if the user is really there
        user = User.objects.get(username = regular_username)
        self.assertIsNotNone(user)
        regular_user = ExtendedUser.objects.get(user=user)
        self.assertEqual(regular_user.user.username, regular_username)
        self.assertEqual(regular_user.user_type, UserType.REGULAR.val)
        
    
    ###########################################################################
    ### user cannot create manager or regular user or superuser
    def test_regular_user_cannot_create_manageruser(self):
        """Regular user cannot create manager user."""
        client = APIClient()
        token = self.create_user_token(client, UserType.REGULAR, "DEFAULT")
        regular_username = "regularuser"
        response = self.request_user_creation(client, UserType.MANAGER, regular_username, token)
        
        # assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # assert that a new user was not created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(ExtendedUser.objects.count(), 1)


    def test_regular_user_cannot_create_regular_user(self):
        """Regular user cannot create regular user."""
        client = APIClient()
        token = self.create_user_token(client, UserType.REGULAR, "DEFAULT")
        regular_username = "regularuser"
        response = self.request_user_creation(client, UserType.REGULAR, regular_username, token)
        
        # assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # assert that a new user was not created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(ExtendedUser.objects.count(), 1)
    
    
    def test_regular_user_cannot_create_superuser(self):
        """Regular user cannot create superuser."""
        client = APIClient()
        token = self.create_user_token(client, UserType.REGULAR, "DEFAULT")
        regular_username = "regularuser"
        response = self.request_user_creation(client, UserType.SUPER, regular_username, token)
        
        # assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
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
        """Test username and password can obtain token and refresh from API"""
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        token_dict = json.loads(self.response.content)
        self.assertTrue('access' in token_dict)
        self.assertTrue('refresh' in token_dict)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token_dict['access']))
        response = self.client.get(
            reverse('location-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_can_log_out(self):
        """Test user can log out and blacklist token on server"""
        # TODO: consider shortening the access token lifespan to a few seconds
        # test out with real dev server outside this testing framework
        # ...or switch to basic token authentication provided by django (reduce dependency)
        
        # log user in
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        token_dict = json.loads(self.response.content)
        self.assertTrue('access' in token_dict)
        self.assertTrue('refresh' in token_dict)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token_dict['access']))
        response = self.client.get(
            reverse('location-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # log user out
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework_simplejwt.tokens import BlacklistMixin
        
        # base64 encoded token string
        token = RefreshToken(token_dict['refresh'])
        print(token)
        print()
        token.blacklist()
        
        class Black(BlacklistMixin, AccessToken):
            pass
            
        token = Black(token_dict['access'])
        print(token)
        token.blacklist()
        token.check_blacklist()
        
        # attempt to log in again should fail
        response = self.client.get(
            reverse('location-list')
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)