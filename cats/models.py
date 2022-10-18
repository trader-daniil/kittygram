from django.db import models
from datetime import date


class Cat(models.Model):
    """Модель кота."""
    BL = 'BLACK'
    WT = 'WHITE'
    OR = 'ORANGE'
    COLOR_CHOICES = (
        (BL, 'Black'),
        (WT, 'White'),
        (OR, 'Orange'),
    )
    color = models.CharField(
        choices=COLOR_CHOICES,
        verbose_name='Цвет шерсти',
        max_length=20,
    )
    name = models.CharField(
        verbose_name='Кличка кота',
        max_length=30,
    )
    birth_year = models.PositiveSmallIntegerField(
        verbose_name='Год рождения кота',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def get_age(self):
        """Получение возрасат кота."""
        if self.birth_year:
            current_year = date.today().year
            return current_year - self.birth_year
        return 'Год рождения не указан'
        
