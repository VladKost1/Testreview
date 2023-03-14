# Generated by Django 4.1.7 on 2023-03-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("src", "0004_alter_datacolumn_options_alter_dataschema_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="datacolumn",
            name="data_schema",
        ),
        migrations.AddField(
            model_name="datacolumn",
            name="data_schema",
            field=models.ManyToManyField(
                to="src.dataschema", verbose_name="Data Schema"
            ),
        ),
    ]