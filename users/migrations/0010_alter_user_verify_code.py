# Generated by Django 4.2.2 on 2024-09-27 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_verify_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verify_code',
            field=models.CharField(default='672058', max_length=6, verbose_name='Код верификации'),
        ),
    ]
