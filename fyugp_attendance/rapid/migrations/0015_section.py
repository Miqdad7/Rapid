# Generated by Django 5.1.5 on 2025-01-31 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0014_alter_teachercourse_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section_id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('part', models.IntegerField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=8)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapid.course')),
            ],
        ),
    ]
