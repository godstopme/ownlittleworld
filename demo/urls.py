from django.urls import path

from demo.views import StartBotView

urlpatterns = [
    path('bot', StartBotView.as_view()),
]
