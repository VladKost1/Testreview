from django.db import models
from users.models import User
from random import randint


class BaseModel(models.Model):
    create_datetime = models.DateTimeField(verbose_name="Creation Datetime", null=True, auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Last Update Datetime", null=True, auto_now=True)

    class Meta:
        abstract = True


class DataSchema(BaseModel):

    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name="data_user", verbose_name="User")
    name = models.CharField(max_length=50, verbose_name="Name")


    class Meta:
        verbose_name = "Data Schema"
        verbose_name_plural = "Data Schemas"

    def __str__(self):
        return self.name


class DataColumn(BaseModel):
    TYPES = (
        ('full_name', 'Full Name'),
        ('job', 'Job'),
        ('email', 'Email'),
        ('domain_name', 'Domain Name'),
        ('phone_number', 'Phone Number'),
        ('company_name', 'Company Name'),
        ('text', 'Text'),
        ('integer', 'Integer'),
        ('address', 'Address'),
        ('date', 'Date'),
    )
    column_name = models.CharField(max_length=255, default='', verbose_name="Column Name")
    column_type = models.CharField(choices=TYPES, default='full_name', max_length=255, verbose_name="Column Type")
    data_schema = models.ForeignKey(to='src.DataSchema', on_delete=models.CASCADE, default=None,
                                    related_name="datacolumn",
                                    verbose_name="Data Schema")
    order_index = models.PositiveSmallIntegerField(default=0, verbose_name="Order Index")
    range_start = models.IntegerField(blank=True, null=True, verbose_name="Range Start")
    range_end = models.IntegerField(blank=True, null=True, verbose_name="Range End")

    class Meta:
        verbose_name = "Data Column"
        verbose_name_plural = "Data Columns"

    def __str__(self):
        return self.column_name

    def generate_data(self):
        pass
