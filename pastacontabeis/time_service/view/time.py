from django.http import HttpRequest, HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from nasajon.util.json_util import JsonUtil
from nasajon.util.objeto_util import ObjetosUtils
from time_service.view.abstract_view import AbstractView
from django.utils.encoding import smart_str
import os
from time_service.entity.redis import Redis
import datetime
from time_service.service.time_service import TimeService
from time_service.util.time_factory import TimeFactory


class TimeView(AbstractView):

    def __init__(self):
        super().__init__()
        self.http_method_names = ['get', "post"]

    def do_get(self, request: HttpRequest, args, kwargs):

        return {"time": TimeService.now().strftime("%Y-%m-%d %H:%M:%S")}

    def do_post(self, request: HttpRequest, args, kwargs):

        dados = JsonUtil().decode(request.body.decode('utf-8'))

        hora_real = datetime.datetime.now()
        hora_arbitrada = dados["time"]

        Redis.getClientInstance().set("hora_real", hora_real.strftime("%Y-%m-%d %H:%M:%S"))
        Redis.getClientInstance().set("hora_arbitrada", hora_arbitrada)

        TimeFactory.getTimeService().inserir(
            datetime.datetime.strptime(hora_arbitrada, "%Y-%m-%d %H:%M:%S"))

        return {}
