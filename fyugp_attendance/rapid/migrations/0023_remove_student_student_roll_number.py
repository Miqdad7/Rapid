# Generated by Django 5.1.5 on 2025-03-05 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0022_remove_student_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_roll_number',
        ),
    ]
