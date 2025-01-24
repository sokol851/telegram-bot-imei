from rest_framework import serializers


class IMEICheckSerializer(serializers.Serializer):
    """ Сериализатор проверки IMEI """
    imei = serializers.CharField(max_length=15)


class IMEICheckResponseSerializer(serializers.Serializer):
    """ Сериализатор ответа проверки IMEI """
    imei = serializers.CharField(max_length=15)
    status = serializers.CharField()
    brand = serializers.CharField(allow_blank=True)
    model = serializers.CharField(allow_blank=True)
