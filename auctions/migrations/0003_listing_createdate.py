# Generated by Django 3.0.3 on 2020-07-10 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200708_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='createDate',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
