# Generated by Django 4.1.7 on 2023-04-06 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocker', '0003_news_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
