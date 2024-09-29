from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестируем привычки."""

    def setUp(self):
        self.user = User.objects.create(email="freeuser@user.ru")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            place="Место",
            time="20:20:20",
            start_date="2024-09-27",
            action="Действие",
            nice_habit=True,
            periodicity="1",
            reward=None,
            time_to_complete=2,
            is_published=True,
            status="created",
            user=self.user,
            related_habit=None
        )

    def test_habit_list(self):
        """Тестируем вывод списка привычек."""

        url = reverse("habit:habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_is_published_list(self):
        """Тестируем вывод списка публичных привычек."""

        url = reverse("habit:published_habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_create(self):
        """Тестируем создание привычки."""
        url = reverse("habit:habit_create")
        data = {
            "action": "Ничего не делать",
            "number_of_executions": 5,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        """Тестируем изменение привычки."""
        url = reverse("habit:habit_update", args=(self.habit.pk,))
        data = {
            "reward": "Почесать за ухом",
            "number_of_executions": 4,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("reward"), "Почесать за ухом")

    def test_habit_delete(self):
        """Тестируем удаление привычки."""
        url = reverse("habit:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
