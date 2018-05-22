from rest_framework import serializers

from memberarea.apps.authentication.serializers import NestedUserSerializer
from memberarea.apps.tags.serializers import TagSerializer
from .models import WorkedHoursStats
from .models import Workitem
from .models import WorkitemAssignment


class NestedWorkitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workitem
        fields = (
            'id', 'title',
        )
        read_only_fields = (
            'id', 'title',
        )


class WorkitemAssignmentSerializer(serializers.ModelSerializer):
    assignee = NestedUserSerializer(read_only=True)
    verified_by = NestedUserSerializer(read_only=True)
    workitem = NestedWorkitemSerializer(read_only=True)

    class Meta:
        model = WorkitemAssignment
        fields = (
            'id', 'assignee', 'duration_real', 'done_at',
            'verified_at', 'verified_by', 'workitem'
        )


class WorkitemSerializer(serializers.ModelSerializer):
    created_by = NestedUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    assignments = WorkitemAssignmentSerializer(read_only=True, many=True)

    class Meta:
        model = Workitem
        fields = (
            'id', 'created_at', 'updated_at', 'title', 'description',
            'published', 'duration_expected', 'due_at', 'max_assignees',
            'created_by', 'tags', 'assignments'
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'created_by', 'tags', 'assignments'
        )


class WorkedHoursStatsSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True)

    class Meta:
        model = WorkedHoursStats
        fields = (
            'user', 'year', 'hoursConfirmed', 'hoursNotConfirmed', 
        )
        read_only_fields = (
            'user', 'year', 'hoursConfirmed', 'hoursNotConfirmed', 
        )
