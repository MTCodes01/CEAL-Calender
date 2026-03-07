from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from clubs.models import Club
from clubs.serializers import ClubSerializer


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile with club details
    """
    club = ClubSerializer(read_only=True)
    sub_club = ClubSerializer(read_only=True)
    extra_clubs = ClubSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'club', 'sub_club', 'extra_clubs', 'notification_enabled', 'notification_time', 'timezone',
            'is_staff', 'is_superuser'
        ]
        read_only_fields = ['id', 'email', 'is_staff', 'is_superuser']


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for admin to update user club assignment
    """
    extra_clubs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Club.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ['club', 'sub_club', 'extra_clubs']

    def update(self, instance, validated_data):
        extra_clubs = validated_data.pop('extra_clubs', None)
        instance = super().update(instance, validated_data)
        if extra_clubs is not None:
            instance.extra_clubs.set(extra_clubs)
        return instance


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user settings
    """
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'notification_enabled',
            'notification_time', 'timezone'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
