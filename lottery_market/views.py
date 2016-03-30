# -*- coding: utf-8 -*-

import pytz
import re
from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lib.langconv import *
from lottery.common import *
from serializers import *


def query_market(src):
    try:
        m = Market.objects.filter(src=src).order_by("-update").first()
        if m is not None and (datetime.now() - m.update).seconds < 300:
            return {
                "update": MarketSerializer(m).data["update"],
                "markets": MarketSerializer(Market.objects.filter(src=src, update=m.update), many=True).data
            }
        else:
            return None
    except ObjectDoesNotExist:
        return None


@api_view(['GET'])
def market(request):
    if "src" in request.GET:
        src = request.GET["src"]
        markets = query_market(src)
        if markets is not None:
            return Response(markets)
        elif src == "5C":
            five(request)
            return Response(query_market(src))
        elif src == "HK":
            hkjc(request)
            return Response(query_market(src))
        elif src == "BF":
            betfair(request)
            return Response(query_market(src))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def five(request):
    url = "http://trade.500.com/jczq/"
    r = re.compile(r"<tr zid=(.*?)fid=\"(.*?)\" homesxname=\"(.*?)\" awaysxname=\"(.*?)\"(.*?)class=\"match_time\" title=\"(.*?)\"(.*?)<div class=\"bet_odds\">(.*?)data-sp=\"(.*?)\"(.*?)data-sp=\"(.*?)\"(.*?)data-sp=\"(.*?)\"(.*?)</div>(.*?)</tr>", re.MULTILINE | re.DOTALL)
    content = load_url(url, "GBK")
    update = datetime.now()
    for m in r.finditer(content):
        fid = m.group(2)
        home_team = m.group(3).replace(" ", "")
        away_team = m.group(4).replace(" ", "")
        match_time = datetime.strptime(m.group(6).replace("开赛时间：", ""), "%Y-%m-%d %H:%M")
        odds = [float(m.group(9)), float(m.group(11)), float(m.group(13))]
        odd = Odd(home=odds[0], draw=odds[1], away=odds[2])
        odd.save()
        game, _ = Market.objects.update_or_create(src='5C', market=fid)
        game.update = update
        game.t = match_time
        game.home = home_team
        game.away = away_team
        game.odd = odd
        game.save()
    return Response(query_market("5C"))


@api_view(['GET'])
def hkjc(request):
    url = "http://bet.hkjc.com/football/index.aspx"
    r = re.compile(r"rmid(.*?)\">(.*?)title=\"對賽往績\">(.*?) <label class='lblvs'>對</label> (.*?)</a></span></td>(.*?)<td class=\"cesst ttgR2\"><span>(.*?)</span></td>(.*?)HAD_H\">(.*?)</span></a></span></td>(.*?)HAD_D\">(.*?)</span></a></span></td>(.*?)HAD_A\">(.*?)</span></a></span></td>", re.MULTILINE | re.DOTALL)
    if "lang" in request.GET and request.GET["lang"] == "en":
        url = "http://bet.hkjc.com/football/index.aspx?lang=" + request.GET["lang"]
        r = re.compile(r"rmid(.*?)\">(.*?)title=\"Head to Head\">(.*?) <label class='lblvs'>vs</label> (.*?)</a></span></td>(.*?)<td class=\"cesst ttgR2\"><span>(.*?)</span></td>(.*?)HAD_H\">(.*?)</span></a></span></td>(.*?)HAD_D\">(.*?)</span></a></span></td>(.*?)HAD_A\">(.*?)</span></a></span></td>", re.MULTILINE | re.DOTALL)
    content = load_url(url)
    update = datetime.now()
    for m in r.finditer(content):
        fid = m.group(1)
        home_team = Converter('zh-hans').convert(m.group(3).decode('utf-8')).encode('utf-8')
        away_team = Converter('zh-hans').convert(m.group(4).decode('utf-8')).encode('utf-8')
        match_time = datetime.strptime(str(date.today().year) + "-" + m.group(6)[3:5] + "-" + m.group(6)[:2] + m.group(6)[5:], "%Y-%m-%d %H:%M")
        odds = [m.group(8), m.group(10), m.group(12)]
        odd = Odd(home=odds[0], draw=odds[1], away=odds[2])
        odd.save()
        game, _ = Market.objects.update_or_create(src='HK', market=fid)
        game.update = update
        game.t = match_time
        game.home = home_team
        game.away = away_team
        game.odd = odd
        game.save()
    return Response(query_market("HK"))


@api_view(['GET'])
def betfair(request):
    update = datetime.now()
    for coupon_id in range(1, 7):
        url = "http://www.betfair.com/exchange/football/coupon?id=" + str(coupon_id)
        r = re.compile(r"<a href=\"/exchange/football/event\?id=(\d*?)\"(.*?)<span class=\"home-team\">(.*?)</span>(.*?)<span class=\"away-team\">(.*?)</span>(.*?)<span class=\"start-time \">(.*?)</span>(.*?)back(.*?)<span class=\"price\">(.*?)</span>(.*?)back(.*?)<span class=\"price\">(.*?)</span>(.*?)back(.*?)<span class=\"price\">(.*?)</span>", re.MULTILINE | re.DOTALL)
        content = load_url(url)
        match_date = re.search("coupon for (.*?)\. Get", content).group(1)
        for m in r.finditer(content):
            try:
                fid = m.group(1)
                home_team = m.group(3)
                away_team = m.group(5)
                match_time = datetime.strptime(match_date + " " + m.group(7)[-5:], "%a %d %b %Y %H:%M").replace(tzinfo=pytz.timezone("Europe/London"))
                odds = [m.group(10).strip(), m.group(13).strip(), m.group(16).strip()]
                odd = Odd(home=odds[0], draw=odds[1], away=odds[2])
                odd.save()
                game, _ = Market.objects.update_or_create(src='BF', market=fid)
                game.update = update
                game.t = match_time
                game.home = home_team
                game.away = away_team
                game.odd = odd
                game.save()
            except ValueError:
                pass
    return Response(query_market("BF"))
