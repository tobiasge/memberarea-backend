from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    pw_expires_at = serializers.DateField()

    class Meta:
        model = User 
        fields = (
            'salutation', 'first_name', 'last_name', 'sex', 'birthday',
            'email', 'member_id', 'entry_date', 'exit_date', 'state',
            'pw_is_expired', 'pw_expires_at', 'id',
        )


class UserPublicSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    pw_expires_at = serializers.DateField()

    class Meta:
        model = User
        fields = (
            'salutation', 'first_name', 'last_name', 'sex',
            'member_id', 'state', 'id',
        )


class NestedUserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of nested User objects."""

    class Meta:
        model = User 
        fields = (
            'id', 'display_name',
        )
