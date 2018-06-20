from django.urls import path

from .views import HandlerView

urlpatterns = [
    path('', HandlerView.as_view(), name='commandHandler'),
]