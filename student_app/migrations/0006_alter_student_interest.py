# Generated by Django 5.2.1 on 2025-05-13 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0005_alter_student_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='interest',
            field=models.TextField(),
        ),
    ]
