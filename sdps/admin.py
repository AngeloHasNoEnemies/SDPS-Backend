from django.contrib import admin
from .models import DrainageLocation, SensorData, Alert, MaintenanceReport

admin.site.register(DrainageLocation)
admin.site.register(SensorData)
admin.site.register(Alert)
admin.site.register(MaintenanceReport)