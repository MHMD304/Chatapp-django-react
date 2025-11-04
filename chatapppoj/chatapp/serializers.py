from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message


#  Serializer for creating users (handles password encryption)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # hide password from responses

    def create(self, validated_data):
        # Use Django's built-in create_user to hash the password automatically
        user = User.objects.create_user(**validated_data)
        return user


#  Serializer for listing users (without password)
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


#  Serializer for conversations
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'participants', 'created_at')

    def to_representation(self, instance):
        # Customize how the conversation is represented (optional)
        representation = super().to_representation(instance)
        return representation


#  Serializer for displaying messages
class MessageSerializer(serializers.ModelSerializer):
    sender = UserListSerializer()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'content', 'timestamp', 'participants')

    def get_participants(self, obj):
        # Retrieve all users participating in the message's conversation
        return UserListSerializer(
            obj.conversation.participants.all(), many=True
        ).data


#  Serializer for creating new messages
class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('conversation', 'sender', 'content')

    def create(self, validated_data):
        # Create a new message in the given conversation
        message = Message.objects.create(**validated_data)
        return message
