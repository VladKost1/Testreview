# Generated by Django 4.1.7 on 2023-03-09 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("src", "0003_rename_order_datacolumn_оrder_index_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="datacolumn",
            options={
                "verbose_name": "Data Column",
                "verbose_name_plural": "Data Columns",
            },
        ),
        migrations.AlterModelOptions(
            name="dataschema",
            options={
                "verbose_name": "Data Schema",
                "verbose_name_plural": "Data Schemas",
            },
        ),
        migrations.RemoveField(
            model_name="datacolumn",
            name="name",
        ),
        migrations.RemoveField(
            model_name="datacolumn",
            name="оrder_index",
        ),
        migrations.AddField(
            model_name="datacolumn",
            name="column_name",
            field=models.CharField(
                default="", max_length=255, verbose_name="Column Name"
            ),
        ),
        migrations.AddField(
            model_name="datacolumn",
            name="order_index",
            field=models.PositiveSmallIntegerField(
                default=0, verbose_name="Order Index"
            ),
        ),
        migrations.AlterField(
            model_name="datacolumn",
            name="column_type",
            field=models.CharField(
                choices=[
                    ("full_name", "Full Name"),
                    ("job", "Job"),
                    ("email", "Email"),
                    ("domain_name", "Domain Name"),
                    ("phone_number", "Phone Number"),
                    ("company_name", "Company Name"),
                    ("text", "Text"),
                    ("integer", "Integer"),
                    ("address", "Address"),
                    ("date", "Date"),
                ],
                default="full_name",
                max_length=255,
                verbose_name="Column Type",
            ),
        ),
        migrations.AlterField(
            model_name="datacolumn",
            name="create_datetime",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Creation Datetime"
            ),
        ),
        migrations.AlterField(
            model_name="datacolumn",
            name="data_schema",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="src.dataschema",
                verbose_name="Data Schema",
            ),
        ),
        migrations.AlterField(
            model_name="datacolumn",
            name="last_update",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Last Update Datetime"
            ),
        ),
        migrations.AlterField(
            model_name="datacolumn",
            name="range_end",
            field=models.IntegerField(blank=True, null=True, verbose_name="Range End"),
        ),
        migrations.AlterField(
            model_name="datacolumn",
            name="range_start",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Range Start"
            ),
        ),
        migrations.AlterField(
            model_name="dataschema",
            name="create_datetime",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Creation Datetime"
            ),
        ),
        migrations.AlterField(
            model_name="dataschema",
            name="last_update",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Last Update Datetime"
            ),
        ),
        migrations.AlterField(
            model_name="dataschema",
            name="name",
            field=models.CharField(max_length=50, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="dataschema",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="data_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
