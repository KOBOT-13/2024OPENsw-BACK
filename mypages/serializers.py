from rest_framework import serializers
from .models import QuizRecord

class QuizRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizRecord
        fields = '__all__'
