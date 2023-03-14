from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from src.models import DataSchema, DataColumn
from src.forms import DataColumnForm, DataSchemaForm, DataColumnFormSet
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv


# Create your views here.

class DataColumnListView(View):
    def get(self, request):
        user_id = request.user.id
        schemas = DataSchema.objects.filter(user_id=user_id)
        context = {
            'schemas': schemas,
        }
        return render(request, 'index.html', context)


class DataColumnDetailView(View):
    def get(self, request, schema_id):
        if self.request.user.is_authenticated:
            schema = DataSchema.objects.get(id=schema_id)
            columns = schema.datacolumn.all().order_by('order_index')
            context = {
                'schema': schema,
                'columns': columns
            }
            return render(request, 'data_column_detail.html', context)
        else:
            return render(request, 'index.html')


class DataSchemaCreateView(CreateView):
    model = DataSchema
    form_class = DataSchemaForm
    success_url = reverse_lazy('data_list')
    template_name = 'data_schema_create.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['data_columns'] = DataColumnFormSet(self.request.POST, instance=self.object)
        else:
            data['data_columns'] = DataColumnFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        data_columns = context['data_columns']
        with transaction.atomic():
            if self.request.user.is_authenticated:
                form.instance.user = self.request.user
                self.object = form.save()
                if data_columns.is_valid():
                    data_columns.instance = self.object
                    data_columns.save()
                return super().form_valid(form)
            else:
                return redirect('login')


class DataColumnCreateView(CreateView):
    model = DataColumn
    form_class = DataColumnForm
    template_name = 'data_column_create.html'

    def get_success_url(self):
        return reverse_lazy('data_detail', kwargs={'schema_id': self.kwargs['data_schema_id']})

    def form_valid(self, form):
        data_schema = get_object_or_404(DataSchema, pk=self.kwargs['data_schema_id'])
        form.instance.data_schema = data_schema
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_schema'] = get_object_or_404(DataSchema, pk=self.kwargs['data_schema_id'])
        return context


class DataColumnUpdateView(UpdateView):
    model = DataColumn
    form_class = DataColumnForm
    template_name = 'data_column_update.html'

    def get_success_url(self):
        return reverse('data_detail', args=[self.object.data_schema.id])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Data column has been updated.')
        return response


class DataSchemaDeleteView(DeleteView):
    model = DataSchema
    template_name = 'data_schema_delete.html'
    success_url = reverse_lazy('data_list')


class DataColumnDeleteView(DeleteView):
    model = DataColumn
    template_name = 'data_column_delete.html'
    success_url = reverse_lazy('data_list')


class DataSchemaDownloadView(View):
    def get(self, request, schema_id):
        schema = DataSchema.objects.get(id=schema_id)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{schema.name}.csv"'

        # get number of rows from request
        num_rows = int(request.GET.get('num_rows', 10))
        # write column headers with order index
        columns = schema.datacolumn.all().order_by('order_index')
        writer = csv.writer(response)
        writer.writerow(['Column_name', 'Column_type', 'Range_start', 'Range_end'])
        columns_fields = columns.values_list('column_name', 'column_type', 'range_start', 'range_end')
        for column in columns_fields:
            writer.writerow(column)
        return response


