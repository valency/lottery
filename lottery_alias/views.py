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
    zh_cn = request.GET["zh_cn"] or None
    zh_tw = request.GET["zh_tw"] or None
    en_hk = request.GET["en_hk"] or None
    en_gb = request.GET["en_gb"] or None
    alias = Alias(zh_cn=zh_cn, zh_tw=zh_tw, en_hk=en_hk, en_gb=en_gb)
    alias.save()
    return Response(AliasSerializer(alias).data)


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
