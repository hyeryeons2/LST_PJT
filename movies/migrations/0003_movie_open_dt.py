# Generated by Django 2.2.7 on 2019-11-25 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20191125_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='open_dt',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
