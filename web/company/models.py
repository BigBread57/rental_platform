from django.db import models

from core.collections import ReservationStatuses


class Company(models.Model):
    """
    Модель компании
    """

    name = models.CharField('Название', max_length=200)
    description = models.CharField('Описание', max_length=2000, blank=True)
    user = models.OneToOneField('user.User', verbose_name='Пользователь', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):

        return self.name


class RentalPoint(models.Model):
    """
    Модель точки выдачи
    """

    schedule = models.JSONField('График', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    is_delivery = models.BooleanField('Есть доставка', default=False, blank=True)
    address = models.ForeignKey(
        'reference.Address', verbose_name='адрес', on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(
        'company.Company', verbose_name='Компания', related_name='rental_points', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Точка выдачи'
        verbose_name_plural = 'Точки выдачи'

    def __str__(self):

        return f'{self.id}: {self.phone}'


class Reservation(models.Model):
    """
    Модель бронирования
    """

    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    count = models.IntegerField('Количество', default=1)
    datetime_from = models.DateTimeField('С', null=True, blank=True)
    datetime_to = models.DateTimeField('До', null=True, blank=True)
    status = models.CharField(
        'Статус', max_length=10, choices=ReservationStatuses.CHOICES, default=ReservationStatuses.NEW)
    offer = models.ForeignKey(
        'offer.Offer', verbose_name='Предложение', related_name='reservations', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        'user.User', verbose_name='Пользователь', related_name='reservations', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Брование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):

        return f'{self.date_created.strftime("%d-%m-%Y %H:%m")} - {self.get_status_display()}'
