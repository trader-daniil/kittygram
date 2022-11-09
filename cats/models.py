from django.db import models
from datetime import date


class Achievement(models.Model):
    """
    Модель действий кота.
    """
    name = models.CharField(
        max_length=128,
        verbose_name='Название действия',
    )


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


COLOR_CHOICES = (
    ('BLACK', 'Black'),
    ('WHITE', 'White'),
    ('ORANGE', 'Orange'),
)

class Cat(models.Model):
    """Модель кота."""
    color = models.CharField(
        choices=COLOR_CHOICES,
        verbose_name='Цвет шерсти',
        max_length=64,
    )
    name = models.CharField(
        verbose_name='Кличка кота',
        max_length=64,
    )
    birth_year = models.PositiveSmallIntegerField(
        verbose_name='Год рождения кота',
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        'Person',
        related_name='cats',
        on_delete=models.CASCADE,
        verbose_name='Хозяин кота',
    )
    achievements = models.ManyToManyField(
        'Achievement',
        verbose_name='Действия, совершенные котом',
        related_name='cats',
    )

    def __str__(self):
        return self.name

    def get_age(self):
        """Получение возрасат кота."""
        if self.birth_year:
            current_year = date.today().year
            return current_year - self.birth_year
        return 'Год рождения не указан'
