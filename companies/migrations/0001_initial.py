# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=120)),
                ('employee_range', models.SmallIntegerField(choices=[(0, b'1-10  employees'), (1, b'10-50 employees'), (2, b'50-500 employees'), (3, b'500-1000 employees'), (4, b'1000-5000 employees'), (5, b'5000-... employees')])),
                ('founded', models.DateField()),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator])),
                ('phone', models.CharField(max_length=30)),
                ('website', models.URLField(validators=[django.core.validators.URLValidator])),
                ('logo', models.ImageField(height_field=50, width_field=50, upload_to='logos/%Y/%m/%d', blank=True)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
    ]
