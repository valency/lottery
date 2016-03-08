import csv
import uuid
from datetime import datetime

import networkx
from celery.result import AsyncResult
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Max, Min
from django.http import HttpResponse
from networkx.readwrite import json_graph
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cache import *
from geometry import *
from serializers import *

MAP_UPLOAD_DIR = "/var/www/html/avatar/data/map/"
TRAJ_UPLOAD_DIR = "/var/www/html/avatar/data/trajectory/"


class TrajectoryViewSet(viewsets.ModelViewSet):
    queryset = Trajectory.objects.all()
    serializer_class = TrajectorySerializer


class RoadViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer


@api_view(['GET'])
def init_road_network_in_memory(request):
    if 'id' in request.GET:
        get_road_network_by_id(request.GET["id"])
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def demo_result(request):
    if 'id' in request.GET:
        result = AsyncResult(request.GET["id"])
        if result.ready():
            return Response({"status": result.ready(), "result": result.get()})
        else:
            return Response({"status": result.ready()})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)