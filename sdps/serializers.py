from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DrainageLocation, SensorData, Alert, MaintenanceReport


# ──────────────────────────────────────────────
# Auth Serializers
# ──────────────────────────────────────────────

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


# ──────────────────────────────────────────────
# Drainage Location Serializers
# ──────────────────────────────────────────────

class DrainageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrainageLocation
        fields = [
            'id', 'name', 'address', 'latitude', 'longitude',
            'status', 'description', 'installed_at', 'updated_at'
        ]
        read_only_fields = ['id', 'installed_at', 'updated_at']


class DrainageLocationSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for dashboard/list views."""
    latest_water_level = serializers.SerializerMethodField()
    active_alerts_count = serializers.SerializerMethodField()

    class Meta:
        model = DrainageLocation
        fields = [
            'id', 'name', 'address', 'status',
            'latest_water_level', 'active_alerts_count', 'updated_at'
        ]

    def get_latest_water_level(self, obj):
        latest = obj.sensor_readings.first()
        return latest.water_level if latest else None

    def get_active_alerts_count(self, obj):
        return obj.alerts.filter(is_resolved=False).count()


# ──────────────────────────────────────────────
# Sensor Data Serializers
# ──────────────────────────────────────────────

class SensorDataSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = SensorData
        fields = [
            'id', 'location', 'location_name',
            'water_level', 'flow_rate', 'blockage_detected',
            'turbidity', 'temperature', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp', 'location_name']

    def validate_water_level(self, value):
        if value < 0:
            raise serializers.ValidationError("Water level cannot be negative.")
        if value > 500:
            raise serializers.ValidationError("Water level exceeds maximum sensor range (500cm).")
        return value

    def validate_flow_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("Flow rate cannot be negative.")
        return value


# ──────────────────────────────────────────────
# Alert Serializers
# ──────────────────────────────────────────────

class AlertSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    resolved_by_username = serializers.CharField(source='resolved_by.username', read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id', 'location', 'location_name', 'alert_type',
            'message', 'severity', 'is_resolved',
            'resolved_at', 'resolved_by', 'resolved_by_username', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'location_name', 'resolved_by_username']


class AlertCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['location', 'alert_type', 'message', 'severity']


# ──────────────────────────────────────────────
# Maintenance Report Serializers
# ──────────────────────────────────────────────

class MaintenanceReportSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    reported_by_username = serializers.CharField(source='reported_by.username', read_only=True)

    class Meta:
        model = MaintenanceReport
        fields = [
            'id', 'location', 'location_name',
            'reported_by', 'reported_by_username',
            'description', 'status', 'technician_notes',
            'date_reported', 'date_resolved'
        ]
        read_only_fields = ['id', 'date_reported', 'reported_by', 'location_name', 'reported_by_username']
