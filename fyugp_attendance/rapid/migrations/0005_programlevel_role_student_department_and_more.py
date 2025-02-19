# Generated by Django 5.1.5 on 2025-01-23 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapid', '0004_department_alter_student_program_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramLevel',
            fields=[
                ('program_level_id', models.AutoField(primary_key=True, serialize=False)),
                ('program_level_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rapid.department'),
        ),
        migrations.AlterField(
            model_name='course',
            name='department_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapid.department'),
        ),
        migrations.AlterField(
            model_name='program',
            name='department_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapid.department'),
        ),
        migrations.AlterField(
            model_name='program',
            name='program_level_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapid.programlevel'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapid.role')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.AutoField(primary_key=True, serialize=False)),
                ('teacher_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapid.department')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapid.user')),
            ],
        ),
    ]
