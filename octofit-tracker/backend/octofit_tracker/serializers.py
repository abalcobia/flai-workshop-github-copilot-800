from rest_framework import serializers
from bson import ObjectId
from .models import User, Team, Activity, Leaderboard, Workout


class ObjectIdField(serializers.Field):
    """Custom field to serialize MongoDB ObjectId to string."""

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError('Invalid ObjectId')


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at']

    def get_id(self, obj):
        return str(obj.pk)


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team', 'team_name', 'avatar', 'fitness_level', 'created_at']

    def get_id(self, obj):
        return str(obj.pk)

    def get_team_name(self, obj):
        if obj.team:
            return obj.team.name
        return None


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'user', 'user_name', 'activity_type', 'duration', 'date', 'notes']

    def get_id(self, obj):
        return str(obj.pk)

    def get_user_name(self, obj):
        return obj.user.name if obj.user else None


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'user_name', 'team_name', 'score', 'rank']

    def get_id(self, obj):
        return str(obj.pk)

    def get_user_name(self, obj):
        return obj.user.name if obj.user else None

    def get_team_name(self, obj):
        if obj.user and obj.user.team:
            return obj.user.team.name
        return None


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'exercises', 'difficulty']

    def get_id(self, obj):
        return str(obj.pk)
