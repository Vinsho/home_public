# Generated by Django 4.1.7 on 2023-03-21 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('klcovany', '0006_alter_device_consumption_alter_device_is_selected_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='klcovany.plant'),
        ),
    ]
