from rest_framework import serializers

from .models import Link
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class LinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields = ('original_link', 'shortened_link', 'creation_date', 'expiration_date', 'private', 'user')


class LinkSerializer1(ModelSerializer):
    class Meta:
        model = Link
        fields = ('original_link', 'shortened_link', 'creation_date', 'expiration_date')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# Register Serializer
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
