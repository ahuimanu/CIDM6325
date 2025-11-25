import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("iso_code", models.CharField(help_text="ISO 3166-1 alpha-2 code (e.g., US, CA, MX)", max_length=2, unique=True)),
                ("name", models.CharField(help_text="Display name for the country", max_length=128)),
                ("iso3_code", models.CharField(blank=True, help_text="Optional ISO alpha-3 code", max_length=3)),
                ("numeric_code", models.CharField(blank=True, help_text="Optional numeric ISO code", max_length=3)),
                ("search_name", models.CharField(db_index=True, help_text="Lowercase friendly name used for searches", max_length=128)),
                ("slug", models.SlugField(help_text="URL-friendly identifier", max_length=64, unique=True)),
                ("latitude", models.FloatField(blank=True, help_text="Representative latitude (optional centroid)", null=True)),
                ("longitude", models.FloatField(blank=True, help_text="Representative longitude (optional centroid)", null=True)),
                ("active", models.BooleanField(default=True, help_text="Whether the country is available for lookups")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(help_text="Canonical city name", max_length=255)),
                ("ascii_name", models.CharField(blank=True, help_text="ASCII-safe variant of the name", max_length=255)),
                ("search_name", models.CharField(db_index=True, help_text="Lowercase normalized name used for search", max_length=255)),
                ("slug", models.SlugField(help_text="URL-friendly identifier unique per country", max_length=255)),
                ("latitude", models.FloatField(blank=True, help_text="Latitude (optional centroid)", null=True)),
                ("longitude", models.FloatField(blank=True, help_text="Longitude (optional centroid)", null=True)),
                ("timezone", models.CharField(blank=True, help_text="Timezone identifier if available", max_length=64)),
                ("population", models.IntegerField(blank=True, help_text="Optional population estimate", null=True)),
                ("active", models.BooleanField(default=True, help_text="Whether the city is available for lookups")),
                ("country", models.ForeignKey(help_text="Country the city belongs to", on_delete=django.db.models.deletion.PROTECT, related_name="cities", to="base.country")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AddConstraint(
            model_name="city",
            constraint=models.UniqueConstraint(fields=("country", "search_name"), name="city_country_search_unique"),
        ),
        migrations.AddConstraint(
            model_name="city",
            constraint=models.UniqueConstraint(fields=("country", "slug"), name="city_country_slug_unique"),
        ),
        migrations.AddIndex(
            model_name="city",
            index=models.Index(fields=["country", "search_name"], name="city_country_search_idx"),
        ),
        migrations.AddIndex(
            model_name="city",
            index=models.Index(fields=["country", "slug"], name="city_country_slug_idx"),
        ),
    ]
