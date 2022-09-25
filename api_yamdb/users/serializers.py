from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class UserSerializerMe(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email', 'first_name', 'last_name', 'bio', 'role',)
        read_only_fields = ('role',)
        model = User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('username "me" is no valid')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
