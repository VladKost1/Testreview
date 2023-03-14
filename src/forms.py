from django import forms
from .models import DataSchema, DataColumn


class DataColumnForm(forms.ModelForm):
    class Meta:
        model = DataColumn
        fields = ('column_name', 'column_type', 'order_index', 'range_start', 'range_end', 'data_schema')


class DataSchemaForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        fields = ('name',)


DataColumnFormSet = forms.inlineformset_factory(DataSchema, DataColumn, form=DataColumnForm, extra=1, can_delete=True)

