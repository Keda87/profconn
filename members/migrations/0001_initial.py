# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import members.models
from django.conf import settings
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('status', models.PositiveSmallIntegerField(default=None, null=True, choices=[(0, 'Unblock'), (1, 'Blocked'), (2, 'Requested'), (3, 'Approved'), (4, 'Declined')])),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('role', models.CharField(max_length=120, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('is_present', models.BooleanField(default=False)),
                ('company', models.ForeignKey(related_name='+', blank=True, to='companies.Company', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=120)),
                ('birth', models.DateField()),
                ('email', models.EmailField(unique=True, max_length=254, validators=[django.core.validators.EmailValidator])),
                ('profile_picture', models.ImageField(upload_to=members.models.profile_stored, blank=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('headline', models.CharField(max_length=120, blank=True)),
                ('bio', models.TextField(blank=True)),
                ('connections', models.ManyToManyField(to='members.Person', through='members.Connection', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='experience',
            name='person',
            field=models.ForeignKey(to='members.Person'),
        ),
        migrations.AddField(
            model_name='connection',
            name='friend',
            field=models.ForeignKey(related_name='friend', to='members.Person'),
        ),
        migrations.AddField(
            model_name='connection',
            name='person',
            field=models.ForeignKey(related_name='requester', to='members.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together=set([('person', 'friend')]),
        ),
    ]
