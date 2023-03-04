from django.urls import path

from .views import (
    SchemaListView,
    SchemaCreateView,
    SchemaEditView,
    DataSetsView,
    Login,
    SchemaDeleteView,
    ColumnsDeleteViews,
)

urlpatterns = [
    path("", Login.as_view(), name="index"),
    path("schemas/", SchemaListView.as_view(), name="schema-list"),
    path("schemas/create/", SchemaCreateView.as_view(), name="schema-create"),
    path("schemas/edit/<int:pk>/", SchemaEditView.as_view(), name="schema-edit"),
    path(
        "schemas/delete/<int:pk>/",
        SchemaDeleteView.as_view(),
        name="schema-delete",
    ),
    path("schemas/<int:pk>/", DataSetsView.as_view(), name="schema-detail"),
    path(
        "columns/<int:pk>/delete/", ColumnsDeleteViews.as_view(), name="columns-delete"
    ),
]

app_name = "test_task"
