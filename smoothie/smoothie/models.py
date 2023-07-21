from django.db import models
from django.contrib.auth.models import User


class Smoothie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SmoothieIngredient(models.Model):
    smoothie = models.ForeignKey(Smoothie, on_delete=models.CASCADE)
    fdc_id = models.IntegerField()
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    grams = models.FloatField(default=0)

    def __str__(self):
        return self.description


class Rating(models.Model):
    smoothie = models.ForeignKey(
        Smoothie, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(i, f'{i} star{"s" if i > 1 else ""}') for i in range(1, 6)])

    def __str__(self):
        return f"{self.user}: {self.rating} stars"
