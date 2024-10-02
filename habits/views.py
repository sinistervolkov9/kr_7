from rest_framework import viewsets, generics
from .models import Habit
from .serializer import HabitSerializer
from .paginators import HabitPaginator
from .permission import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Возвращает публичные привычки для всех пользователей и все привычки для их владельцев.
        """
        user = self.request.user

        if user.is_authenticated:
            # Если пользователь аутентифицирован, возвращаем его привычки и публичные
            return Habit.objects.filter(user=user) | Habit.objects.filter(is_published=True)
        else:
            # Если пользователь не аутентифицирован, возвращаем только публичные привычки
            return Habit.objects.filter(is_published=True)

    def perform_create(self, serializer):
        """
        При создании привычки автоматически присваиваем её владельцу текущего пользователя.
        """
        serializer.save(user=self.request.user)


class PublicHabitsListView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_published=True)
    serializer_class = HabitSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly],
    # pagination_class = HabitPaginator
