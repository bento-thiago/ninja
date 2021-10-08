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
from time_service.service.time_service import TimeService, TimeRepository
from time_service.util.time_factory import TimeFactory
from time_service.forms.time_form import TimeForm


class TimePageView(AbstractView):

    def __init__(self):
        super().__init__()
        self.http_method_names = ['get', "post"]

    def get(self, request: HttpRequest, *args, **kwargs):
        time = TimeService.now()
        form = TimeForm(data={"time": time})
        return render(request, 'time.html', {"form": form})

    def post(self, request: HttpRequest, *args, **kwargs):

        form = TimeForm(request.POST)

        if form.is_valid():

            hora_real = datetime.datetime.now()
            hora_arbitrada = form.cleaned_data.get(
                "time").strftime("%Y-%m-%d %H:%M:%S")

            Redis.getClientInstance().set("hora_real", hora_real.strftime("%Y-%m-%d %H:%M:%S"))
            Redis.getClientInstance().set("hora_arbitrada", hora_arbitrada)

            TimeFactory.getTimeService().inserir(
                datetime.datetime.strptime(hora_arbitrada, "%Y-%m-%d %H:%M:%S"))

        return render(request, 'time.html', {"form": form})
