# Generated by Django 4.0 on 2021-12-27 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_plannedlesson_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='student_payment',
            field=models.IntegerField(default=350),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_payment',
            field=models.IntegerField(default=200),
        ),
    ]