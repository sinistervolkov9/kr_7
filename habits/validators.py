from datetime import timedelta
from rest_framework.exceptions import ValidationError


class AssociatedWithoutRewardValidator:
    """
    Исключаем одновременный выбор связанной привычки и указания вознаграждения.
    """

    def __call__(self, data):
        habit_reward = data.get('reward')
        habit_related_habit = data.get('related_habit')

        if habit_reward and habit_related_habit:
            raise ValidationError("Нельзя заполнять одновременно вознаграждение и связанную привычку.")


class TimeToCompleteValidator:
    """
    Время выполнения должно быть не больше 120 секунд.
    """

    def __call__(self, data):
        habit_time_to_complete = data.get('time_to_complete')

        if habit_time_to_complete:
            if habit_time_to_complete > 2:
                raise ValidationError("Время на выполнение должно быть не больше 2 минут (120 секунд).")


class RelatedHabitValidator:
    """
    В связанные привычки могут попадать только привычки с признаком приятной привычки.
    """

    def __call__(self, data):
        habit_related_habit = data.get('related_habit')

        if habit_related_habit and not data.related_habit.nice_habit:
            raise ValidationError("Связанная привычка должна быть приятной привычкой.")


class NiceHabitRewardValidator:
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """

    def __call__(self, data):
        habit_nice_habit = data.get('nice_habit')
        habit_reward = data.get('reward')
        habit_related_habit = data.get('related_habit')

        if habit_nice_habit and (habit_reward or habit_related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")


class PeriodicityValidator:
    """
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    Нельзя не выполнять привычку более 7 дней.
    """

    def __call__(self, data):
        habit_periodicity = data.get('periodicity')

        if habit_periodicity and int(habit_periodicity) > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
        if habit_periodicity and int(habit_periodicity) < 1:
            raise ValidationError("Привычка должна выполняться хотя бы раз в 7 дней.")
