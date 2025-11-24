from django.db import models

class SearchRecord(models.Model):
    continent = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    capital = models.CharField(max_length=100, null=True, blank=True)
    population = models.BigIntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.country} ({self.capital}) - {self.continent}"