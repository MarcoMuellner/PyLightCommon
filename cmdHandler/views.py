from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from PyLightCommon.cmdHandler.cmdHandler import handler

@method_decorator(csrf_exempt, name='dispatch')
class HandlerView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        return handler.inCmd(request.GET["commando"])

    def post(self, request: WSGIRequest) -> HttpResponse:
        return handler.inCmd(request.POST["commando"])
