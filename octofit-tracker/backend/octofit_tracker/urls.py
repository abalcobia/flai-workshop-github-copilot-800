"""octofit_tracker URL Configuration"""
import os
from django.conf import settings as django_settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    api_root, UserViewSet, TeamViewSet, ActivityViewSet,
    LeaderboardViewSet, WorkoutViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

# Base URL for the REST API endpoints.
# When running in a GitHub Codespace the proxy rewrites the host, so
# USE_X_FORWARDED_HOST / SECURE_PROXY_SSL_HEADER in settings.py ensure
# request.build_absolute_uri() returns the correct HTTPS URL below.
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

# Expose base_url via REST_FRAMEWORK settings so serialisers and
# hyperlinked fields can discover the correct API root at runtime.
if not getattr(django_settings, 'REST_FRAMEWORK', None):
    django_settings.REST_FRAMEWORK = {}
django_settings.REST_FRAMEWORK.setdefault('DEFAULT_API_BASE_URL', base_url)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('', api_root, name='api-root-home'),
]
