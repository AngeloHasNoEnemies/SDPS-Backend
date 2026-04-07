from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import DrainageLocation, SensorData, Alert, MaintenanceReport
from .serializers import (
    RegisterSerializer, UserSerializer,
    DrainageLocationSerializer, DrainageLocationSummarySerializer,
    SensorDataSerializer,
    AlertSerializer, AlertCreateSerializer,
    MaintenanceReportSerializer,
)


# ──────────────────────────────────────────────
# Auth Views
# ──────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ──────────────────────────────────────────────
# Drainage Location Views
# ──────────────────────────────────────────────

class DrainageLocationViewSet(viewsets.ModelViewSet):
    queryset = DrainageLocation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return DrainageLocationSummarySerializer
        return DrainageLocationSerializer

    @action(detail=True, methods=['get'])
    def sensor_data(self, request, pk=None):
        location = self.get_object()
        readings = location.sensor_readings.all()[:50]
        serializer = SensorDataSerializer(readings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def alerts(self, request, pk=None):
        location = self.get_object()
        alerts = location.alerts.filter(is_resolved=False)
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


# ──────────────────────────────────────────────
# Sensor Data Views
# ──────────────────────────────────────────────

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.select_related('location').all()
    serializer_class = SensorDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        location_id = self.request.query_params.get('location')
        if location_id:
            qs = qs.filter(location_id=location_id)
        return qs


# ──────────────────────────────────────────────
# Alert Views
# ──────────────────────────────────────────────

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.select_related('location', 'resolved_by').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return AlertCreateSerializer
        return AlertSerializer

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user
        alert.save()
        return Response(AlertSerializer(alert).data)


# ──────────────────────────────────────────────
# Maintenance Report Views
# ──────────────────────────────────────────────

class MaintenanceReportViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceReport.objects.select_related('location', 'reported_by').all()
    serializer_class = MaintenanceReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)