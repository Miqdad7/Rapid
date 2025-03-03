# Generated by Django 5.1.5 on 2025-01-23 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_code', models.CharField(max_length=20, unique=True)),
                ('course_title', models.CharField(max_length=100)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=4)),
                ('department_id', models.IntegerField()),
                ('strength', models.IntegerField()),
                ('semester', models.IntegerField()),
            ],
        ),
    ]
