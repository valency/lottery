# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('a', models.CharField(max_length=36)),
                ('b', models.CharField(max_length=36)),
            ],
        ),
    ]
