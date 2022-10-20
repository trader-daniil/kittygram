from django.db import models
from datetime import date



class Person(models.Model):
    """
    Модель человека.
    """
    ML = 'MALE'
    FM = 'FEMALE'
    NB = 'NON-BINARY'
    SEX_CHOICES = (
        (ML, 'Male'),
        (FM, 'Female'),
        (NB, 'Non-binary'),
    )
    first_name = models.CharField(
        verbose_name='Имя человека',
        max_length=256,
    )
    last_name = models.CharField(
        verbose_name='Фамилия человека',
        max_length=256,
    )
    sex = models.CharField(
        choices=SEX_CHOICES,
        verbose_name='Пол человека',
        max_length=128,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



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
    owner = models.ForeignKey(
        'Owner',
        related_name='cats',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Хозяин кота',
    )

    def __str__(self):
        return self.name

    def get_age(self):
        """Получение возрасат кота."""
        if self.birth_year:
            current_year = date.today().year
            return current_year - self.birth_year
        return 'Год рождения не указан'
        
