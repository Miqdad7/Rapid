# Generated by Django 5.1.5 on 2025-02-04 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0017_remove_course_strength'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='year_offered',
        ),
    ]
