# Generated by Django 5.0.2 on 2024-02-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maintenance_app", "0005_maintenanceschedule_technique"),
    ]

    operations = [
        migrations.AddField(
            model_name="maintenanceschedule",
            name="title",
            field=models.CharField(default="plan de maintenance", max_length=200),
        ),
    ]