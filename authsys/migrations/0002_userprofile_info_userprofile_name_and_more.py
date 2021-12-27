# Generated by Django 4.0 on 2021-12-27 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authsys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='info',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='surname',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
