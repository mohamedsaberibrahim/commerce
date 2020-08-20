# Generated by Django 3.0.3 on 2020-07-10 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200710_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='imageUrl',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listingState',
            field=models.BooleanField(default=True),
        ),
    ]
