from rest_framework import serializers
from .models import Habit
from .validators import (
    AssociatedWithoutRewardValidator,
    TimeToCompleteValidator,
    RelatedHabitValidator,
    NiceHabitRewardValidator,
    PeriodicityValidator
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        # Проверка: нельзя указать одновременно и вознаграждение, и связанную привычку
        AssociatedWithoutRewardValidator()(data)

        # Валидация времени выполнения: не более 120 минут
        TimeToCompleteValidator()(data)

        # Связанная привычка должна быть только с приятной привычкой
        NiceHabitRewardValidator()(data)

        # Проверка периодичности на выполнение привычки (не реже 1 раза в неделю)
        PeriodicityValidator()(data)

        return data

    def create(self, validated_data):
        return Habit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
