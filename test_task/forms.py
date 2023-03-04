from django import forms
from extra_views import InlineFormSetFactory

from test_task.models import Schema, Column, DataSet


class SchemaForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Write name of schema"})
    )

    class Meta:
        model = Schema
        fields = "__all__"
        widgets = {"user": forms.HiddenInput()}


class ColumnForm(forms.ModelForm):
    column_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Write column name"}),
    )

    class Meta:
        model = Column
        fields = "__all__"


class SchemaColumnInline(InlineFormSetFactory):
    model = Column
    form_class = ColumnForm

    fields = "__all__"

    factory_kwargs = {
        "extra": 1,
        "max_num": None,
        "can_order": False,
        "can_delete": False,
    }


class DataSetForm(forms.ModelForm):
    rows = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "input rows"}),
    )

    class Meta:
        model = DataSet
        fields = ("rows",)
