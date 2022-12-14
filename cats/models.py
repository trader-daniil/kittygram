from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Achievement(models.Model):
    """
    Модель действий кота.
    """
    name = models.CharField(
        max_length=128,
        verbose_name='Название действия',
    )


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
        User,
        related_name='cats',
        on_delete=models.CASCADE,
        verbose_name='Хозяин кота',
    )
    achievements = models.ManyToManyField(
        'Achievement',
        verbose_name='Действия, совершенные котом',
        related_name='cats',
    )

    constraints = (
        models.UniqueConstraint(
            fields=('owner', 'name'),
            name='unique_owners_cat',
        ),
    )

    def __str__(self):
        return self.name

    def get_age(self):
        """Получение возрасат кота."""
        if self.birth_year:
            current_year = date.today().year
            return current_year - self.birth_year
        return 'Год рождения не указан'
