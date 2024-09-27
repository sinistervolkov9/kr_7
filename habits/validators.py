from datetime import timedelta
from rest_framework.exceptions import ValidationError


class AssociatedWithoutRewardValidator:
    """
    Исключаем одновременный выбор связанной привычки и указания вознаграждения.
    """

    def __call__(self, habit):
        if habit.reward and habit.related_habit:
            raise ValidationError("Нельзя заполнять одновременно вознаграждение и связанную привычку.")


class TimeToCompleteValidator:
    """
    Время выполнения должно быть не больше 120 секунд.
    """

    def __call__(self, habit):
        if habit.time_to_complete:
            if habit.time_to_complete > 2:
                raise ValidationError("Время на выполнение должно быть не больше 2 минут (120 секунд).")

class RelatedHabitValidator:
    """
    В связанные привычки могут попадать только привычки с признаком приятной привычки.
    """

    def __call__(self, habit):
        if habit.related_habit and not habit.related_habit.nice_habit:
            raise ValidationError("Связанная привычка должна быть приятной привычкой.")


class NiceHabitRewardValidator:
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """

    def __call__(self, habit):
        if habit.nice_habit and (habit.reward or habit.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")


class PeriodicityValidator:
    """
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    Нельзя не выполнять привычку более 7 дней.
    """

    def __call__(self, habit):
        if habit.periodicity and int(habit.periodicity) > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
        if habit.periodicity and int(habit.periodicity) < 1:
            raise ValidationError("Привычка должна выполняться хотя бы раз в 7 дней.")
