# Generated by Django 4.2.2 on 2024-09-27 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(blank=True, help_text='Укажите место, в котором необходимо выполнять привычку', max_length=50, null=True, verbose_name='Место')),
                ('time', models.TimeField(blank=True, help_text='Установите время, когда необходимо выполнять привычку', null=True, verbose_name='Время')),
                ('action', models.CharField(help_text='Укажите действие, которое представляет собой привычка', max_length=50, verbose_name='Действие')),
                ('nice_habit', models.BooleanField(blank=True, default=True, help_text='Это привычка, которую можно привязать к выполнению полезной привычки?', null=True, verbose_name='Признак приятной привычки')),
                ('periodicity', models.IntegerField(default=1, help_text='Укажите периодичность выполнения привычки для напоминания в днях (по умолчанию ежедневная)', verbose_name='Периодичность')),
                ('reward', models.CharField(blank=True, null=True, verbose_name='Вознаграждение')),
                ('time_to_complete', models.TimeField(blank=True, null=True, verbose_name='Время на выполнение')),
                ('is_published', models.BooleanField(blank=True, default=True, null=True, verbose_name='Признак публичности')),
                ('related_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habits.habit', verbose_name='Связанная привычка')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Пользователь', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
            },
        ),
    ]
