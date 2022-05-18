from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class LatitudeField(models.DecimalField):
    """Поле модели для широты"""

    def __init__(self, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'Широта')
        kwargs['max_digits'] = kwargs.get('max_digits', 20)
        kwargs['decimal_places'] = kwargs.get('decimal_places', 18)
        kwargs['validators'] = kwargs.get('validators', [MinValueValidator(-90), MaxValueValidator(90)])
        super().__init__(**kwargs)


class LongitudeField(models.DecimalField):
    """Поле модели для долготы"""

    def __init__(self, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'Долгота')
        kwargs['max_digits'] = kwargs.get('max_digits', 21)
        kwargs['decimal_places'] = kwargs.get('decimal_places', 18)
        kwargs['validators'] = kwargs.get('validators', [MinValueValidator(-180), MaxValueValidator(180)])
        super().__init__(**kwargs)


class AbstractImage(models.Model):
    """Абстрактрая модель изображения"""

    name = models.CharField('Название', max_length=2000, blank=True)
    image = models.FileField('Файл', upload_to='images')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.image.url}'
