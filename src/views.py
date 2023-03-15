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
from faker import Faker
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
        return reverse_lazy('data_list')

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
        writer.writerow([column.column_name for column in columns])
        fake = Faker()
        for i in range(num_rows):
            row_data = []
            for column in columns:
                if column.column_type == 'full_name':
                    row_data.append(fake.name())
                elif column.column_type == 'job':
                    row_data.append(fake.job())
                elif column.column_type == 'email':
                    row_data.append(fake.email())
                elif column.column_type == 'domain_name':
                    row_data.append(fake.domain_name())
                elif column.column_type == 'phone_number':
                    row_data.append(fake.phone_number())
                elif column.column_type == 'company_name':
                    row_data.append(fake.company())
                elif column.column_type == 'text':
                    row_data.append(fake.text())
                elif column.column_type == 'integer':
                    row_data.append(fake.random_int(min=column.range_start, max=column.range_end))
                elif column.column_type == 'address':
                    row_data.append(fake.address())
                elif column.column_type == 'date':
                    row_data.append(fake.date())
            writer.writerow(row_data)
        return response





# def generate_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="people.csv"'
#
#     writer = csv.writer(response)
#     writer.writerow(['Name', 'Email', 'Phone', 'Address', 'Date of Birth'])
#
#     fake = Faker()
#
#     for i in range(100):
#         name = fake.name()
#         email = fake.email()
#         phone = fake.phone_number()
#         address = fake.address()
#         date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
#
#         writer.writerow([name, email, phone, address, date_of_birth.strftime('%Y-%m-%d')])
#
#         person = Person(name=name, email=email, phone=phone, address=address, date_of_birth=date_of_birth)
#         person.save()
#
#     return response

