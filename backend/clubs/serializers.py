from rest_framework import serializers
from .models import Club


class ClubSerializer(serializers.ModelSerializer):
    """
    Serializer for Club model including nested sub-clubs
    """
    sub_clubs = serializers.SerializerMethodField()
    
    class Meta:
        model = Club
        fields = ['id', 'slug', 'name', 'color', 'parent', 'order', 'sub_clubs']
        read_only_fields = ['id']

    def get_sub_clubs(self, obj):
        # Only return sub_clubs for main clubs to avoid deep recursion if not needed
        # and sort by the 'order' field
        if not obj.parent:
            sub_clubs = obj.sub_clubs.all().order_by('order', 'name')
            return ClubSerializer(sub_clubs, many=True).data
        return []
