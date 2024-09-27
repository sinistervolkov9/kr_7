from django.contrib import admin
from habits.models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'time', 'place', 'user',)
    list_filter = ('id',)
