# Generated by Django 5.0.2 on 2024-02-28 19:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maintenance_app", "0013_equipmentcategory_equipment_cost_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="equipment",
            name="used_by",
            field=models.CharField(
                choices=[
                    ("option1", "Department"),
                    ("option2", "Employee"),
                    ("option3", "Other"),
                ],
                default="option1",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="CorrectiveMaintenance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("scheduled_date", models.DateField()),
                (
                    "maintenance_duration",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                (
                    "equipment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="maintenance_app.equipment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Technician",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.CharField(max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MaintenanceRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "maintenance_type",
                    models.CharField(
                        choices=[
                            ("corrective", "Corrective Maintenance"),
                            ("preventive", "Preventive Maintenance"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "equipment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="maintenance_app.equipment",
                    ),
                ),
                (
                    "preventive_maintenance",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="maintenance_app.preventivemaintenance",
                    ),
                ),
                (
                    "technician",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="maintenance_app.technician",
                    ),
                ),
            ],
        ),
    ]
