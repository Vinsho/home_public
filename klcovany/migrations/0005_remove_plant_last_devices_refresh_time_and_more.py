# Generated by Django 4.1.7 on 2023-03-21 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klcovany', '0004_plant_device_plant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='last_devices_refresh_time',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='last_surplus_refresh_time',
        ),
        migrations.AddField(
            model_name='plant',
            name='last_refresh',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]