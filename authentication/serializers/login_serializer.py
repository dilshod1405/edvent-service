from rest_framework import serializers
from django.contrib.auth import authenticate
from authentication.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # username or email
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid credentials or inactive account.")
        
        data['user'] = user
        return data
