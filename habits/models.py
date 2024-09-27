from django.db import models
from django.conf import settings
from django.utils import timezone
from .validators import (
    AssociatedWithoutRewardValidator,
    TimeToCompleteValidator,
    RelatedHabitValidator,
    NiceHabitRewardValidator,
    PeriodicityValidator,
)

NULLABLE = {"blank": True, "null": True}
PERIODICITY_CHOICES = (
    ('1', 'Каждый 1 день'),
    ('2', 'Каждые 2 дня'),
    ('3', 'Каждые 3 дня'),
    ('4', 'Каждые 4 дня'),
    ('5', 'Каждые 5 дней'),
    ('6', 'Каждые 6 дней'),
    ('7', 'Каждые 7 дней'),
)
STATUS_CHOICES = (
    ('created', 'Создана'),
    ('active', 'Активна'),
    ('completed', 'Завершена'),
)


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=50,
        verbose_name="Место",
        help_text="Укажите место, в котором необходимо выполнять привычку",
        **NULLABLE
    )
    time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Время",
        help_text="Установите время, когда необходимо выполнять привычку",
        **NULLABLE
    )
    start_date = models.DateField(
        default=timezone.now,
        verbose_name="Дата начала",
        help_text="Установите дату, когда необходимо приступить к выполнению привычки",
        **NULLABLE
    )
    action = models.CharField(
        max_length=50,
        verbose_name="Действие",
        help_text="Укажите действие, которое представляет собой привычка",
    )
    nice_habit = models.BooleanField(
        default=True,
        verbose_name="Признак приятной привычки",
        help_text="Это привычка, которую можно привязать к выполнению полезной привычки?",
        **NULLABLE
    )
    related_habit = models.ForeignKey(
        "self",
        verbose_name="Связанная привычка",
        on_delete=models.CASCADE,
        **NULLABLE
    )
    periodicity = models.CharField(
        default='1',
        max_length=50,
        verbose_name="Периодичность",
        help_text="Повторять...",
        choices=PERIODICITY_CHOICES
    )
    reward = models.CharField(
        verbose_name="Вознаграждение",
        **NULLABLE
    )
    time_to_complete = models.PositiveIntegerField(
        default=1,
        verbose_name="Время на выполнение (в минутах)",
        **NULLABLE
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Признак публичности",
        **NULLABLE
    )
    status = models.CharField(
        default='created',
        max_length=50,
        verbose_name='Статус',
        choices=STATUS_CHOICES,
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        super().clean()

        validators = [
            AssociatedWithoutRewardValidator(),
            TimeToCompleteValidator(),
            RelatedHabitValidator(),
            NiceHabitRewardValidator(),
            PeriodicityValidator(),
        ]

        for validator in validators:
            validator(self)
