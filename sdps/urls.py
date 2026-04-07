from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = DefaultRouter()
router.register(r'locations', views.DrainageLocationViewSet, basename='location')
router.register(r'sensor-data', views.SensorDataViewSet, basename='sensordata')
router.register(r'alerts', views.AlertViewSet, basename='alert')
router.register(r'maintenance', views.MaintenanceReportViewSet, basename='maintenance')

urlpatterns = [
    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', obtain_auth_token, name='login'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),

    # Resources
    path('', include(router.urls)),
]