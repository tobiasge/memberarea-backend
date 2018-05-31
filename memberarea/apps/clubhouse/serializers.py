from rest_framework import serializers

from memberarea.apps.authentication.serializers import NestedUserSerializer
from .models import Clubhouse, Room, Defect


class ClubhouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clubhouse
        fields = (
            'id', 'name',
        )
        read_only_fields = (
            'id', 'name',
        )


class RoomSerializer(serializers.ModelSerializer):
    clubhouse = ClubhouseSerializer(read_only=True)

    class Meta:
        model = Room
        fields = (
            'id', 'name', 'clubhouse',
        )
        read_only_fields = (
            'id', 'name', 'clubhouse',
        )


class DefectSerializer(serializers.ModelSerializer):
    clubhouse = ClubhouseSerializer(read_only=True)
    room = ClubhouseSerializer(read_only=True)
    reported_by = NestedUserSerializer(read_only=True)

    class Meta:
        model = Defect
        fields = (
            'id', 'title', 'clubhouse', 'room', 'description', 'reported_by', 'repaired',
        )
        read_only_fields = (
            'id', 'clubhouse', 'room', 'reported_by',
        )
