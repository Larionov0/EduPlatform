# Generated by Django 4.0 on 2022-06-09 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_lesson_date_start_alter_lesson_time_start_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='C_s_min',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='C_t_min',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='p_s_ser',
            field=models.FloatField(default=5),
        ),
        migrations.AddField(
            model_name='company',
            name='p_t_ser',
            field=models.FloatField(default=6),
        ),
        migrations.AddField(
            model_name='student',
            name='presence_chance',
            field=models.IntegerField(default=100),
        ),
    ]
