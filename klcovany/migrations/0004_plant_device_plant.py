# Generated by Django 4.1.7 on 2023-03-21 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('klcovany', '0003_device_consumption'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128)),
                ('meter_id', models.CharField(max_length=128)),
                ('energy_surplus', models.IntegerField()),
                ('last_surplus_refresh_time', models.TimeField()),
                ('last_devices_refresh_time', models.TimeField()),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='plant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='klcovany.plant'),
            preserve_default=False,
        ),
    ]
