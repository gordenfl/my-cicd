from django.shortcuts import render
from .models import User
from .models import Song
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, SongSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

@csrf_exempt
def GetLatestSongs(request):
    pass

class MyView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': "user_id does not exist"}, status=status.HTTP_)