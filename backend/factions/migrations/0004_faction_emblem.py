# Generated by Django 3.2.7 on 2021-09-24 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factions', '0003_auto_20210924_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='faction',
            name='emblem',
            field=models.ImageField(blank=True, null=True, upload_to='faction_emblems'),
        ),
    ]