import csv

from django.conf import settings
from faker import Faker

from .models import DataSet, Schema, Column


def generate_fake_data(type_: int, range_=(0, 100)) -> str:
    fake = Faker()
    fake_data = {
        "Full_name": fake.name(),
        "Job": fake.job(),
        "Email": fake.email(),
        "Domain_name": fake.email().split("@")[-1],
        "Phone_number": fake.phone_number(),
        "Company_name": fake.company(),
        "Text": fake.sentences(nb=fake.random_int(min=range_[0], max=range_[1])),
        "Integer": fake.random_int(*range_),
        "Address": fake.address(),
        "Date": fake.date(),
    }
    return fake_data[type_]


def generate_csv_file(dataset: DataSet) -> None:
    schema = Schema.objects.get(id=dataset.schema.id)
    columns = Column.objects.filter(schema=schema).order_by("order").values()

    delimiter = schema.column_separator
    quote = schema.string_character

    csv.register_dialect(
        "custom",
        delimiter=delimiter,
        quotechar=quote,
        quoting=csv.QUOTE_ALL,
    )

    headers = [column["column_name"] for column in columns]

    with open(
        settings.MEDIA_ROOT + f"/schema{schema.title}_dataset{dataset.id}.csv",
        "w",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=headers, dialect="custom")
        writer.writeheader()

        for row in range(dataset.rows):

            row = {}
            for column in columns:
                value = generate_fake_data(column["data_type"])
                row[column["column_name"]] = value

            writer.writerow(row)
    dataset.status = 1
    dataset.download_link = (
        f"{settings.MEDIA_URL}schema{schema.title}_dataset{dataset.id}.csv"
    )
    dataset.save()
