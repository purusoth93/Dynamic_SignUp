# Generated by Django 5.1 on 2025-02-19 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_doctor_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
