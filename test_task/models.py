from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Schema(models.Model):

    DELIMITERS = [
        (",", "Comma(,)"),
        (";", "Semilicon(;)"),
        (" ", "Space( )"),
        ("|", "Pipe(|)"),
    ]

    QUOTES = [
        ('"', 'Double-quote(")'),
        ("'", "Single-quote(')"),
    ]

    title = models.CharField(max_length=63, blank=True, null=True)
    column_separator = models.TextField(choices=DELIMITERS, default=",", max_length=1)
    string_character = models.TextField(choices=QUOTES, default='""', max_length=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="schemas"
    )

    def get_absolute_url(self):
        return reverse("test_task:schema-detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ["-updated"]


class Column(models.Model):

    DATA_TYPES = [
        ("Full_name", "Full name"),
        ("Job", "Job"),
        ("Email", "Email"),
        ("Domain_name", "Domain name"),
        ("Phone_number", "Phone number"),
        ("Company_name", "Company name"),
        ("Text", "Text"),
        ("Integer", "Integer"),
        ("Address", "Address"),
        ("Date", "Date"),
    ]

    column_name = models.CharField(max_length=20)
    data_type = models.CharField(max_length=20, choices=DATA_TYPES)
    order = models.PositiveIntegerField(default=0)
    schema = models.ForeignKey(
        to=Schema, on_delete=models.CASCADE, related_name="schemacolumns"
    )

    class Meta:
        ordering = ["order"]

    def clean(self):
        super(Column, self).clean()
        if not self.order:
            self.order = Column.objects.filter(schema=self.schema).count() + 1


class DataSet(models.Model):
    STATUSES = [(0, "Processing.."), (1, "Ready!")]
    schema = models.ForeignKey(
        to=Schema, on_delete=models.CASCADE, related_name="schemadatasets"
    )
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=0)
    rows = models.PositiveIntegerField(null=True)
    download_link = models.URLField()

    class Meta:
        ordering = ["-created"]
