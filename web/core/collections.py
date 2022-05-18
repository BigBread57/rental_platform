class TimeUnits:
    """
    Класс-коллекция единиц измерения срока аренды
    """

    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'

    CHOICES = (
        (MINUTE, 'минута'),
        (HOUR, 'час'),
        (DAY, 'день')
    )


class ReservationStatuses:
    """
    Класс-коллекция статусов бронирования
    """

    NEW = 'new'
    ACCEPTED = 'accepted'
    CANCELED = 'canceled'
    DECLINED = 'declined'
    DONE = 'done'

    CHOICES = (
        (NEW, 'Новая'),
        (ACCEPTED, 'Принята'),
        (CANCELED, 'Отменена'),
        (DECLINED, 'Отклонена'),
        (DONE, 'Выполнена')
    )
