from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    quantity = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0, 'Quantity should be >=0')]
                                   )
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.IntegerField(default=0,
                                validators=[MinValueValidator(0, 'Quantity should be >=0')]
                                )

    def __str__(self):
        return f'{self.name} {self.quantity}'

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с товаром
        return f'/products/{self.id}'


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    text = models.TextField()
    date = models.DateField()
    time = models.TimeField()
