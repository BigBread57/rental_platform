from django.db import models


class Product(models.Model):
    """
    Модель предмета аренды
    """

    name = models.CharField('Наименование', max_length=200)
    category = models.ForeignKey(
        'reference.Category', verbose_name='Категория', related_name='products', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):

        return self.name
