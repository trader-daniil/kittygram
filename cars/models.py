from django.db import models

class Car(models.Model):
    """Модель автомобиля."""
    name = models.CharField(
        verbose_name='Название машины',
        max_length=128,
    )
    color = models.CharField(
        verbose_name='Цвет автомобиля',
        max_length=128,
    )
    description = models.TextField(verbose_name='Описание машины')
    type = models.IntegerField(
        choices=(
            (1, "Sedan"),
            (2, "Truck"),
            (4, "SUV"),
        ),
        verbose_name='Тип кузова автомобиля',
    )
