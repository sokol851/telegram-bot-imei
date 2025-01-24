from rest_framework import serializers


class IMEICheckSerializer(serializers.Serializer):
    """ Сериализатор проверки IMEI """
    imei = serializers.CharField(max_length=15)
