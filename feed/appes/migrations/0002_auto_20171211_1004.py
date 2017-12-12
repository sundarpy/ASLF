# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-11 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sublink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_name', models.CharField(blank=True, db_index=True, default=b'', max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='myfeed',
            name='sub_link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appes.Sublink'),
        ),
    ]
