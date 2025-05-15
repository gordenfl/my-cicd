from django.shortcuts import render
from .models import User
from .models import Song
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, SongSerializer

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongSViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()