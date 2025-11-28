from rest_framework import serializers
from .models import Event
from clubs.serializers import ClubSerializer


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model
    """
    club = ClubSerializer(read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start', 'end', 'location',
            'club', 'created_by', 'created_by_email', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'club', 'created_by', 'created_at', 'updated_at']
    
    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.username
    
    def validate(self, data):
        """
        Validate that end time is after start time
        """
        if data.get('end') and data.get('start'):
            if data['end'] <= data['start']:
                raise serializers.ValidationError({
                    "end": "End time must be after start time."
                })
        return data


class EventCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating events (club is auto-filled from user)
    """
    class Meta:
        model = Event
        fields = ['title', 'description', 'start', 'end', 'location']
    
    def validate(self, data):
        """
        Validate that end time is after start time
        """
        if data['end'] <= data['start']:
            raise serializers.ValidationError({
                "end": "End time must be after start time."
            })
        return data
