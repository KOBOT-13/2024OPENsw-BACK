import os
import json
from rest_framework import serializers
from .models import *

class AudioTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioText
        fields = '__all__'