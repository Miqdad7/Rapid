# Generated by Django 5.1.5 on 2025-03-05 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0021_hourdatecourse_absentdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='gender',
        ),
    ]
