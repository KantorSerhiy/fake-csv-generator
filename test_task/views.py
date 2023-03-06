from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpRequest, FileResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin, DeleteView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from test_task.utils import generate_csv_file

from test_task.forms import (
    SchemaForm,
    SchemaColumnInline,
    DataSetForm,
)
from test_task.models import Schema, DataSet, Column


class Login(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class SchemaListView(LoginRequiredMixin, generic.ListView):
    model = Schema
    queryset = Schema.objects.all()
    template_name = "core/schema_list.html"

    def get_queryset(self):
        queryset = Schema.objects.filter(user=self.request.user)
        return queryset


class SchemaCreateView(LoginRequiredMixin, CreateWithInlinesView):
    model = Schema
    form_class = SchemaForm
    inlines = [
        SchemaColumnInline,
    ]
    template_name = "core/schema_form.html"

    def get_initial(self):
        return {"user": self.request.user}

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "add_column":
                return reverse_lazy(
                    "test_task:schema-edit", kwargs={"pk": self.object.pk}
                )
            if self.request.POST["action"] == "submit":
                return reverse_lazy("test_task:schema-list")
        return reverse_lazy("test_task:schema-list")


class SchemaEditView(LoginRequiredMixin, UpdateWithInlinesView):
    model = Schema
    form_class = SchemaForm
    inlines = [
        SchemaColumnInline,
    ]
    template_name = "core/schema_form.html"

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "add_column":
                return reverse_lazy(
                    "test_task:schema-edit", kwargs={"pk": self.object.pk}
                )
            if self.request.POST["action"] == "submit":
                return reverse_lazy("test_task:schema-list")
        return reverse_lazy("test_task:schema-list")


class SchemaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Schema
    template_name = "core/schema_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("test_task:schema-list")


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


class DataSetsView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Schema
    form_class = DataSetForm
    template_name = "core/datasets.html"

    def get_context_data(self, **kwargs):
        context = super(DataSetsView, self).get_context_data()
        schema = self.get_object()
        columns = schema.schemacolumns.all()
        context["columns"] = columns
        return context

    def post(self, request, *args, **kwargs):
        schema = self.get_object()
        dataset = DataSet.objects.create(schema=schema, rows=int(request.POST["rows"]))

        if is_ajax(request):
            generate_csv_file(dataset)

            html = render_to_string(
                "core/table.html",
                context={"schema": schema},
                request=request,
            )

            return JsonResponse({"msg": html})

        return HttpResponseRedirect(
            reverse_lazy("test_task:schema-detail", kwargs={"pk": schema.pk})
        )


class ColumnsDeleteViews(LoginRequiredMixin, generic.DeleteView):
    model = Column
    success_url = reverse_lazy("test_task:schema-create")
