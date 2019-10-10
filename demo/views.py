from rest_framework import views, permissions, status
from rest_framework.response import Response

from demo import tasks
from demo.serializers import ScheduleBotSerializer


class StartBotView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        config = ScheduleBotSerializer(data=self.request.data)
        config.is_valid(raise_exception=True)
        config = config.validated_data

        tasks.run_bot.delay(config)

        return Response(status=status.HTTP_202_ACCEPTED)
