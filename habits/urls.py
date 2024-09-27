from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, PublicHabitsListView

router = DefaultRouter()
router.register(r'habits', HabitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('public/', PublicHabitsListView.as_view(), name='public_habits')
    # path('api', include(router.urls)),
]
