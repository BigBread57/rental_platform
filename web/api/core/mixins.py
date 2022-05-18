from typing import Dict

from rest_framework.serializers import Serializer


class MultiSerializerViewSetMixin:
    """
    Примесь для возможности использования нескольких сериализаторов в одном наборе представлений
    e.g. serializer_map = {'retrieve': RetrieveSerializer, 'list': ListSerializer}
    """

    serializer_map: Dict[str, Serializer] = {}

    def get_serializer_class(self):
        try:
            return self.serializer_map[self.action]

        except (KeyError, AttributeError):
            return super().get_serializer_class()
