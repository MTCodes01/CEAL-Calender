from rest_framework import serializers
from .models import Club


class ClubSerializer(serializers.ModelSerializer):
    """
    Serializer for Club model
    """
    class Meta:
        model = Club
        fields = ['id', 'slug', 'name', 'color', 'parent']
        read_only_fields = ['id']
