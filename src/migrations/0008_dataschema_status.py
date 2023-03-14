# Generated by Django 4.1.7 on 2023-03-13 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("src", "0007_alter_datacolumn_data_schema"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataschema",
            name="status",
            field=models.CharField(
                choices=[("processing", "Processing"), ("ready", "Ready")],
                default="processing",
                max_length=50,
            ),
        ),
    ]
