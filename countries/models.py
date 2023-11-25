from django.db import models
from cities_light.abstract_models import AbstractCity, AbstractCountry


class country(AbstractCountry):
    flag = models.ImageField(upload_to='countries/flags/',null=True,blank=True)
    nationality = models.CharField(max_length=150, null=True, blank=True, help_text="like Egyptian, etc..")
    isFeatured = models.BooleanField(default=False)
    popularity = models.PositiveBigIntegerField(default=0)
class city(AbstractCity):
    isFeatured = models.BooleanField(default=False)
    popularity = models.PositiveBigIntegerField(default=0)
