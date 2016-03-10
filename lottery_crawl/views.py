from rest_framework.decorators import api_view
from rest_framework.response import Response

from lottery.lottery import *


@api_view(['GET'])
def list_lottery_500(request):
    return Response(Lottery500.list())


@api_view(['GET'])
def list_macau_slot(request):
    return Response(MacauSlot.list())
