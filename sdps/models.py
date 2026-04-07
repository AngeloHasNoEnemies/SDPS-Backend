from django.db import models
from django.contrib.auth.models import User


class DrainageLocation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField(blank=True)
    installed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SensorData(models.Model):
    location = models.ForeignKey(
        DrainageLocation, on_delete=models.CASCADE, related_name='sensor_readings'
    )
    water_level = models.FloatField(help_text="Water level in cm")
    flow_rate = models.FloatField(null=True, blank=True, help_text="Flow rate in L/s")
    blockage_detected = models.BooleanField(default=False)
    turbidity = models.FloatField(null=True, blank=True, help_text="Turbidity in NTU")
    temperature = models.FloatField(null=True, blank=True, help_text="Temperature in Celsius")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.location.name} - {self.timestamp}"


class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('flood', 'Flood Warning'),
        ('blockage', 'Blockage Detected'),
        ('sensor_fault', 'Sensor Fault'),
        ('maintenance', 'Maintenance Required'),
    ]
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    location = models.ForeignKey(
        DrainageLocation, on_delete=models.CASCADE, related_name='alerts'
    )
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_alerts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.alert_type} at {self.location.name}"


class MaintenanceReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    location = models.ForeignKey(
        DrainageLocation, on_delete=models.CASCADE, related_name='maintenance_reports'
    )
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='maintenance_reports'
    )
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    technician_notes = models.TextField(blank=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_reported']

    def __str__(self):
        return f"Report for {self.location.name} - {self.status}"