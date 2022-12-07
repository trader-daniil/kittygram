# Generated by Django 4.1.2 on 2022-11-08 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0007_alter_cat_achievements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='color',
            field=models.CharField(choices=[('BLACK', 'Black'), ('WHITE', 'White'), ('ORANGE', 'Orange')], max_length=64, verbose_name='Цвет шерсти'),
        ),
        migrations.AlterField(
            model_name='cat',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Кличка кота'),
        ),
    ]