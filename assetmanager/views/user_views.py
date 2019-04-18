from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from jsonschema import ValidationError
from jsonschema import validate

from ..tests.schemas.utils import load_json_schema

from django.contrib.auth.models import User
from ..models.user_models import ExtendedUser
from .. import permissions


class UserCreate(APIView):
    
    def post(self, request, format=None):
        if not request.data:
            return Response("no data given in request", status.HTTP_400_BAD_REQUEST)
        data = request.data
        json_schema = load_json_schema("user_create.json")
        try:
            validate(data, json_schema)
            # jsonschema not validating property matches, so...
            if not data['password'] == data['confirmPassword']:
                raise ValidationError("Password confirmation does not match password.")
        except ValidationError as err:
            print(err.message)
            return Response(err.message, status.HTTP_400_BAD_REQUEST)
        
        # check permissions
        if not permissions.can_create_user(request.user, data['user_type']):
            return Response("You do not have permission to create this type of user.", status.HTTP_403_FORBIDDEN)
        
        user = User.objects.create_user(
            username = data['username'],
            email = None,
            password = data['password']
        )
        manager_user = ExtendedUser.objects.create(
            user=user,
            department=data['department'],
            user_type=data['user_type'])
        
        permissions.set_permissions_group(user, data['user_type'])
        
        msg = "<Some representation of successfully created user object here>"
        return Response(msg, status.HTTP_201_CREATED)
    
    
class UserLogout(APIView):
    """Takes a JWT token and blacklists it for extra security on the server side.
    For example, the client may forget/fail to remove JWT token from local storage while logging out.
    
    Returns: response status with message detailing success or failure"""
    def post(self, request, format=None):
        # TODO: get base64_encoded_token_string from request.data
        token = RefreshToken(base64_encoded_token_string)
        token.blacklist()
        # TODO: test that unexpired token no longer authenticates the user because it has been blacklisted