import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


def welcome(request):
    return render(request,'home.html')

@api_view(['POST'])
def create_user(request):
    try:
        data = json.loads(request.body)
    except:
        return Response("Provide username, email and password in the request body", status=status.HTTP_400_BAD_REQUEST)
    if "username" in data.keys() and "email" in data.keys() and "password" in data.keys():
        try:
            user_object = User.objects.create(username=data['username'], 
                                            email=data['email'], 
                                            password=make_password(data['password']))
        except:
            return Response('Username exists, please use different username')
        token_key = Token.objects.filter(user_id=user_object.id).first()
        return Response("Token: " + str(token_key))
    else:
        return Response("Provide username, email and password in the request body, either of them is not provided.", status=status.HTTP_400_BAD_REQUEST)