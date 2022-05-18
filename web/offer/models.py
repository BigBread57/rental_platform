from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.collections import TimeUnits
from core.models import AbstractImage


class Offer(models.Model):
    """
    Модель предложения
    """

    is_active = models.BooleanField('Активное', default=True)
    description = models.CharField('Описание', max_length=2000, blank=True)
    count = models.IntegerField('Количество')
    is_for_child = models.BooleanField('Для детей', default=False)
    is_female = models.BooleanField('Для женщин', default=False)
    is_male = models.BooleanField('Для мужчин', default=False)
    is_unisex = models.BooleanField('Унисекс', default=False)
    product = models.ForeignKey(
        'product.Product', verbose_name='Предмет аренды', on_delete=models.SET_NULL, null=True, blank=True)
    rental_point = models.ForeignKey(
        'company.RentalPoint', verbose_name='Точка выдачи', on_delete=models.CASCADE,
        related_name='offers')
    images = models.ManyToManyField('offer.OfferImage', verbose_name='Изображения', related_name='+', blank=True)

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'

    def __str__(self):
        return f'{self.description[:30]}: {self.count}'


class Price(models.Model):
    """
    Модель цены
    """

    time_from = models.IntegerField('Время от')
    time_from_unit = models.CharField(
        'Единица измерения', max_length=10, choices=TimeUnits.CHOICES, default=TimeUnits.HOUR)
    price_per_time = models.FloatField('Цена за единицу времени')
    price_per_time_unit = models.CharField(
        'Единица измерения', max_length=10, choices=TimeUnits.CHOICES, default=TimeUnits.HOUR)
    offer = models.ForeignKey(
        'offer.Offer', verbose_name='Предложение', related_name='prices', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'

    def __str__(self):
        return f'От {self.time_from} {self.time_from_unit} цена: {self.price_per_time} за {self.price_per_time_unit}'


class Rating(models.Model):
    """
    Модель рейтинга предложения
    """

    mark = models.SmallIntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField('Комментарий', max_length=2000, blank=True)
    offer = models.ForeignKey(
        'offer.Offer', related_name='ratings', verbose_name='Предложение', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'{self.mark}'


class OfferImage(AbstractImage):
    """
    Модель изображения предложения
    """

    pass

