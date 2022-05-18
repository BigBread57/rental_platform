from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):
    """
    Класс необходим для отображение человеко-читаемых значений choices в сериализаторах
    """

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]


class ReadOnlySerializer(serializers.Serializer):
    """
    Сериализатор только на чтение
    """

    class Meta:
        fields = '__all__'
        read_only_fields = fields

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class SimpleNameSerializer(ReadOnlySerializer):
    """
    Сериализатор для представление пары id, name
    """

    id = serializers.ReadOnlyField()
    name = serializers.CharField()

    class Meta:
        fields = ('id', 'name')
