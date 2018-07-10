# -*- coding: utf-8 -*-

import re
from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lib.langconv import *
from .serializers import *


def market(src):
    try:
        m = Market.objects.filter(src=src).order_by("-update").first()
        if m is not None and (datetime.now() - m.update).seconds < 300:
            log("Request market source " + src + " cached.")
            return {
                "update": MarketSerializer(m).data["update"],
                "markets": MarketSerializer(Market.objects.filter(src=src, update=m.update), many=True).data
            }
        else:
            log("Request market source " + src + " not cached.")
            return None
    except ObjectDoesNotExist:
        return None


def five():
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
    return market("5C")


def hkjc(lang):
    url = "http://nicpu1.cse.ust.hk/lottery/hkjc/football/index.aspx?lang=" + lang
    if lang == "en":
        r = re.compile(r"rmid(.*?)\">(.*?)title=\"Head to Head\">(.*?) <label class='lblvs'>vs</label> (.*?)</a></span></td>(.*?)<td class=\"cesst ttgR2\"><span>(.*?)</span></td>(.*?)HAD_H\">(.*?)</span></a></span></td>(.*?)HAD_D\">(.*?)</span></a></span></td>(.*?)HAD_A\">(.*?)</span></a></span></td>", re.MULTILINE | re.DOTALL)
    elif lang == "ch":
        r = re.compile(r"rmid(.*?)\">(.*?)title=\"對賽往績\">(.*?) <label class='lblvs'>對</label> (.*?)</a></span></td>(.*?)<td class=\"cesst ttgR2\"><span>(.*?)</span></td>(.*?)HAD_H\">(.*?)</span></a></span></td>(.*?)HAD_D\">(.*?)</span></a></span></td>(.*?)HAD_A\">(.*?)</span></a></span></td>", re.MULTILINE | re.DOTALL)
    else:
        return None
    content = load_url(url)
    update = datetime.now()
    for m in r.finditer(content):
        fid = m.group(1)
        home_team = Converter('zh-hans').convert(m.group(3)).encode('utf8')
        away_team = Converter('zh-hans').convert(m.group(4)).encode('utf8')
        match_time = datetime.strptime(str(date.today().year) + "-" + m.group(6)[3:5] + "-" + m.group(6)[:2] + m.group(6)[5:], "%Y-%m-%d %H:%M")
        odds = [m.group(8), m.group(10), m.group(12)]
        odd = Odd(home=odds[0], draw=odds[1], away=odds[2])
        odd.save()
        game, _ = Market.objects.update_or_create(src='HK-' + lang.upper(), market=fid)
        game.update = update
        game.t = match_time
        game.home = home_team
        game.away = away_team
        game.odd = odd
        game.save()
    return market("HK-" + lang.upper())


def betfair():
    update = datetime.now()
    weekday = (datetime.today().weekday() + 2) % 7
    for coupon_id in range(weekday, weekday + 3):
        for page in range(1, 3):
            try:
                url = "http://nicpu1.cse.ust.hk/lottery/betfair/exchange/football/coupon?goingInPlay=true&id=" + str(coupon_id) + "&fdcPage=" + str(page)
                log("BetFair: " + url)
                r = re.compile(r"<a href=\"/exchange/football/event\?id=(\d*?)\"(.*?)<span class=\"home-team\">(.*?)</span>(.*?)<span class=\"away-team\">(.*?)</span>(.*?)<span class=\"start-time \">(.*?)</span>(.*?)back(.*?)<span class=\"price\">(.*?)</span>(.*?)back(.*?)<span class=\"price\">(.*?)</span>(.*?)back(.*?)<span class=\"price\">(.*?)</span>", re.MULTILINE | re.DOTALL)
                content = load_url(url)
                match_date = re.search("coupon for (.*?)\. Get", content).group(1)
                for m in r.finditer(content):
                    try:
                        fid = m.group(1)
                        home_team = m.group(3)
                        away_team = m.group(5)
                        match_time = datetime.strptime(match_date + " " + m.group(7)[-5:], "%a %d %b %Y %H:%M")
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
            except:
                pass
    return market("BF")


@api_view(['GET'])
def search(request):
    if "src" in request.GET:
        src = request.GET["src"]
        if "home" in request.GET:
            keyword = request.GET["home"]
            m = Market.objects.filter(src=src, home=keyword)
        elif "away" in request.GET:
            keyword = request.GET["away"]
            m = Market.objects.filter(src=src, away=keyword)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if m is not None:
            return Response(MarketSerializer(m, many=True).data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def query(request):
    if "src" in request.GET:
        src = request.GET["src"]
        markets = market(src)
        if markets is not None:
            return Response(markets)
        else:
            return crawl(request)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def crawl(request):
    if "src" in request.GET:
        src = request.GET["src"]
        if src == "5C":
            return Response(five())
        elif src == "HK-CH":
            return Response(hkjc("ch"))
        elif src == "HK-EN":
            return Response(hkjc("en"))
        elif src == "BF":
            return Response(betfair())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
