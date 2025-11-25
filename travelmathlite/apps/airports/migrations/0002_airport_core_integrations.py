import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
        ("airports", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="airport",
            name="active",
            field=models.BooleanField(default=True, help_text="Whether the airport is active/open"),
        ),
        migrations.AddField(
            model_name="airport",
            name="city",
            field=models.ForeignKey(blank=True, help_text="Normalized City derived from municipality", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="airports", to="base.city"),
        ),
        migrations.AddField(
            model_name="airport",
            name="country",
            field=models.ForeignKey(blank=True, help_text="Normalized Country linked via iso_country", null=True, on_delete=django.db.models.deletion.PROTECT, related_name="airports", to="base.country"),
        ),
        migrations.AddIndex(
            model_name="airport",
            index=models.Index(fields=["country"], name="airports_c_country_91032d_idx"),
        ),
        migrations.AddIndex(
            model_name="airport",
            index=models.Index(fields=["city"], name="airports_c_city_9a0fa2_idx"),
        ),
        migrations.AddIndex(
            model_name="airport",
            index=models.Index(fields=["active"], name="airports_c_active_368e1b_idx"),
        ),
    ]
