# Generated by Django 3.1.5 on 2021-07-05 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0003_auto_20210705_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subito',
            name='Price',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
