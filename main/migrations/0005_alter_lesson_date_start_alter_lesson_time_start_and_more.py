# Generated by Django 4.0 on 2021-12-27 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_course_student_payment_course_teacher_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='date_start',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='time_start',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='plannedlesson',
            name='time_start',
            field=models.TimeField(),
        ),
    ]