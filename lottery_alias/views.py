# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from serializers import *


@api_view(['GET'])
def list_alias(request):
    return Response(AliasSerializer(Alias.objects.all(), many=True).data)


@api_view(['GET'])
def add_alias(request):
    if "s" in request.GET:
        s = list(set(request.GET["s"].split(",")))
        if "id" in request.GET:
            try:
                alias = Alias.objects.get(id=request.GET["id"])
                alias.list = alias.list.append(s)
                alias.save()
                return Response(AliasSerializer(alias).data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            alias = Alias(list=s)
            alias.save()
            return Response(AliasSerializer(alias).data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def delete_alias(request):
    if "id" in request.GET:
        try:
            Alias.objects.get(id=request.GET["id"]).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
