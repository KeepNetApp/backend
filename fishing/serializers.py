from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from fishing.models import UserSpeciesStats


class UserSpeciesStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpeciesStats
        fields = (
            "species_id",
            "total_caught",
            "first_catch_id",
            "max_weight_catch_id",
            "max_length_catch_id",
        )

# Sync Serializers

class CatchPhotoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    photo_url = serializers.URLField()
    is_primary = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField()

class CatchSyncSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    species_id = serializers.UUIDField()
    session_id = serializers.UUIDField(required=False, allow_null=True)
    location = GeometryField()
    time_caught = serializers.DateTimeField()
    weight_kg = serializers.FloatField(required=False, allow_null=True)
    length_m = serializers.FloatField(required=False, allow_null=True)
    photos = CatchPhotoSerializer(many=True)

class CatchesSyncSerializer(serializers.Serializer):
    catches = CatchSyncSerializer(many=True)

class CatchSyncResponseSerializer(serializers.Serializer):
    synced = serializers.ListField(child=serializers.UUIDField())
    skipped = serializers.ListField(child=serializers.UUIDField())
    stats = UserSpeciesStatsSerializer(many=True)

class SessionSyncSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    visibility = serializers.ChoiceField(choices=["PRIVATE", "FRIENDS", "PUBLIC"])
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)

class SessionsSyncSerializer(serializers.Serializer):
    sessions = SessionSyncSerializer(many=True)

class SessionSyncResponseSerializer(serializers.Serializer):
    synced = serializers.ListField(child=serializers.UUIDField())
    skipped = serializers.ListField(child=serializers.UUIDField())
