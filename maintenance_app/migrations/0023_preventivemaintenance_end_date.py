# Generated by Django 5.0.2 on 2024-03-06 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "maintenance_app",
            "0022_remove_preventivemaintenance_maintenance_duration_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="preventivemaintenance",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
