import os
from rest_framework import serializers
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *

def home(request):
    return render(request, 'pages/pages.html')

class AudioTextView(APIView):
    
    def get(self, request):
        audiotexts = AudioText.objects.all()
        serializer = AudioTextSerializer(audiotexts, many=True)
        return Response(serializer.data)