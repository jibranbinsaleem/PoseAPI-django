from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, APIKey

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_superuser', 'date_joined', 'firebase_id']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

class GenerateApiKeySerializer(serializers.Serializer):
    # username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    firebase_id = serializers.CharField(max_length=100)

    def validate(self, data):
        # username = data.get('username')
        email = data.get('email')
        firebase_id = data.get('firebase_id')

        try:
            user = User.objects.get(email=email, firebase_id=firebase_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        return data
