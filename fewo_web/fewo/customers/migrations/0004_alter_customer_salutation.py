from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0003_customer_custom_salutation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="salutation",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---"),
                    ("Herr", "Herr"),
                    ("Frau", "Frau"),
                    ("Divers", "Divers"),
                    ("Familie", "Familie"),
                ],
                default="",
                max_length=20,
                verbose_name="Anrede",
            ),
        ),
    ]
