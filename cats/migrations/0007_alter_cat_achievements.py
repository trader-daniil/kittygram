# Generated by Django 4.1.2 on 2022-10-21 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0006_cat_achievements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='achievements',
            field=models.ManyToManyField(related_name='cats', to='cats.achievement', verbose_name='Действия, совершенные котом'),
        ),
    ]
