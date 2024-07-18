from rest_framework import serializers
from .models import QuizRecord, ConversationRecord

class QuizRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizRecord
        fields = '__all__'

class ConversationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationRecord
        fields = '__all__'