from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IMEICheckSerializer
from .services import flow_get_info


class CheckIMEIView(APIView):
    """ Представление для проверки IMEI """
    permission_classes = [AllowAny]  # Разрешаем любые запросы
    authentication_classes = []

    def post(self, request):
        serializer = IMEICheckSerializer(data=request.data)
        if serializer.is_valid():
            imei = serializer.validated_data['imei']
            return Response(flow_get_info(imei), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
