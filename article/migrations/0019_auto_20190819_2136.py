# Generated by Django 2.0.3 on 2019-08-19 21:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0018_auto_20190819_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 19, 21, 36, 33, 384962), help_text='发布日期', verbose_name='发布日期'),
        ),
    ]
