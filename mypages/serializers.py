from rest_framework import serializers

from books.serializers import MainPageBookSerializer
from .models import QuizRecord

class QuizRecordSerializer(serializers.ModelSerializer):
    book = MainPageBookSerializer(read_only=True)
    class Meta:
        model = QuizRecord
        fields = '__all__'

class QuizRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizRecord
        fields = ['id', 'book', 'score']
