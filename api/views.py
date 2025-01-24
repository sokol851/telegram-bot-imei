from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IMEICheckSerializer
from .tasks import check_imei_task


class CheckIMEIView(APIView):
    """ Представление для проверки IMEI """

    def post(self, request):
        serializer = IMEICheckSerializer(data=request.data)
        if serializer.is_valid():
            imei = serializer.validated_data['imei']
            # Запускаем асинхронную задачу
            task = check_imei_task.delay(imei)
            return Response({'task_id': task.id},
                            status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
