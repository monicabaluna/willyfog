# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-16 13:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('willy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('scheduled_date', models.DateTimeField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='willy.Device')),
            ],
        ),
    ]
