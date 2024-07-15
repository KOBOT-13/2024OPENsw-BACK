from django.shortcuts import render
from rest_framework import viewsets
from pages.models import Page
from pages.serializers import PageSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
# Create your views here.
