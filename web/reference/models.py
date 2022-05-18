from django.db import models

from core.models import LatitudeField, LongitudeField


class City(models.Model):
    """
    Модель города
    """

    name = models.CharField('Название', max_length=200)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Address(models.Model):
    """
    Модель адреса
    """

    address = models.CharField('Адрес', max_length=1000, blank=True)
    latitude = LatitudeField(null=True, blank=True)
    longitude = LongitudeField(null=True, blank=True)
    city = models.ForeignKey('City', verbose_name='Город', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address or self.city.name if self.city else 'Не указан'


class Category(models.Model):
    """
    Модель категории
    """

    name = models.CharField('Название', max_length=200)
    parent = models.ForeignKey(
        'self', verbose_name='Категория верхнего уровня', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
