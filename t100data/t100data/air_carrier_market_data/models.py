from django.db import models

# Create your models here.
class MarketData(models.Model):
    id = models.AutoField(primary_key=True)
    passengers = models.IntegerField()
    freight = models.IntegerField()
    mail = models.IntegerField()
    distance = models.IntegerField()
    carrier_id = models.CharField(max_length=3)
    carrier_name = models.TextField()
    orig_airport_id = models.IntegerField()
    orig_iata_code = models.CharField(max_length=3)
    orig_city_name = models.TextField()
    orig_state_abr = models.TextField(max_length=2)
    dest_airport_id = models.IntegerField()
    dest_iata_code = models.CharField(max_length=3)
    dest_city_name = models.TextField()
    dest_state_abr = models.TextField(max_length=2)
    month = models.IntegerField(default=0)
