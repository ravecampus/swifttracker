# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(default=b'', max_length=120, choices=[(b'developer', b'developer'), (b'designer', b'designer')])),
                ('birthdate', models.DateField(null=True)),
                ('phone', models.CharField(max_length=11, null=True, blank=True)),
                ('address', models.CharField(max_length=120, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=2000)),
                ('position', models.CharField(max_length=2000, choices=[(b'developer', b'developer'), (b'designer', b'designer')])),
                ('weekly_hours', models.IntegerField()),
                ('username', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('date_track', models.DateField()),
                ('question1', models.CharField(max_length=2000)),
                ('question2', models.CharField(max_length=2000)),
                ('question3', models.CharField(max_length=2000)),
                ('time_track', models.CharField(max_length=2000)),
                ('project_name', models.ForeignKey(to='accounts.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
