# Generated by Django 5.0.2 on 2024-02-18 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maintenance_app", "0009_maintenanceschedule_duration_hours"),
    ]

    operations = [
        migrations.CreateModel(
            name="Events",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("start", models.DateTimeField(blank=True, null=True)),
                ("end", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "tblevents",
            },
        ),
    ]