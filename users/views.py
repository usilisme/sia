# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from users.serializers import UserSerializer
from users.models import User


#API
class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	
#OVERRIDING DRF-JWT method
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'role': user.Role,
        #'user': UserSerializer(user, context={'request': request}).data
    }
