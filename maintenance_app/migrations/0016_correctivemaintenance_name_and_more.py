# Generated by Django 5.0.2 on 2024-03-04 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maintenance_app", "0015_alter_piecerechange_prix"),
    ]

    operations = [
        migrations.AddField(
            model_name="correctivemaintenance",
            name="name",
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="preventivemaintenance",
            name="name",
            field=models.CharField(default="preventive -", max_length=50),
        ),
    ]
