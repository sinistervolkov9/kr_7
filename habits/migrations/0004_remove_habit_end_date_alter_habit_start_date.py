# Generated by Django 4.2.2 on 2024-09-27 15:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_habit_end_date_habit_start_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='end_date',
        ),
        migrations.AlterField(
            model_name='habit',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, help_text='Установите дату, когда необходимо приступить к выполнению привычки', null=True, verbose_name='Дата начала'),
        ),
    ]
