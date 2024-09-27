from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from habits.views import HabitViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include('users.urls')),

    path('admin/', admin.site.urls),
    path('api/', include((router.urls, "api"), namespace='api')),

    path('users/', include('users.urls')),
    path('habits/', include('habits.urls')),
]

#  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
