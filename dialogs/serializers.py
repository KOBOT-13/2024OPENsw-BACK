from rest_framework import serializers
from .models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField()
    character_name = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = ['id', 'book', 'book_title', 'character', 'character_name', 'created_at']

    def get_book_title(self, obj):
        return obj.book.title

    def get_character_name(self, obj):
        return obj.character.name


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
    
    def validate(self, data):
        sender_type = data.get('sender_type')
        user_sender = data.get('user_sender')
        character_sender = data.get('character_sender')

        if sender_type == 'user' and not user_sender:
            raise serializers.ValidationError("sender_type is 'user', but user_sender is not set.")
        if sender_type == 'character' and not character_sender:
            raise serializers.ValidationError("sender_type is 'character', but character_sender is not set.")
        if sender_type == 'user' and character_sender:
            raise serializers.ValidationError("sender_type is 'user', but character_sender is set.")
        if sender_type == 'character' and user_sender:
            raise serializers.ValidationError("sender_type is 'character', but user_sender is set.")

        return data

