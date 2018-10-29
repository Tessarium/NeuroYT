from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Recognise(models.Model):
    counter_cars = models.IntegerField(default=0, blank=False,
                                       validators=[MaxValueValidator(100), MinValueValidator(0)],
                                       verbose_name="Обнаружено автомобилей")
    created = models.DateTimeField(auto_now_add=True)
