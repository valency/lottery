import re
from datetime import datetime

from deeputils.common import log
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.langconv import *
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
    r = re.compile(r'<tr class="bet-tb-tr" data-fixtureid="(.*?)" data-infomatchid="(.*?)" data-homesxname="(.*?)" data-awaysxname="(.*?)" data-matchdate="(.*?)" data-matchtime="(.*?)"(.*?)data-type="nspf" data-value="(.*?)" data-sp="(.*?)">(.*?)data-type="nspf" data-value="(.*?)" data-sp="(.*?)">(.*?)data-type="nspf" data-value="(.*?)" data-sp="(.*?)">', re.MULTILINE | re.DOTALL)
    content = load_url(url, "GBK")
    update = datetime.now()
    for m in r.finditer(content):
        if '未开售' in m.group(0):
            continue
        fid = m.group(1)
        home_team = m.group(3).replace(" ", "")
        away_team = m.group(4).replace(" ", "")
        match_time = datetime.strptime(m.group(5) + ' ' + m.group(6), "%Y-%m-%d %H:%M")
        odds = [float(m.group(9)), float(m.group(12)), float(m.group(15))]
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
    # TODO
    url = "http://nicpu1.cse.ust.hk:9001/lottery/hkjc/football/getJSON.aspx?jsontype=index.aspx"
    print(requests.Session().get(url).content.decode('UTF-8'))
    content = load_json(url)
    update = datetime.now()
    for m in content:
        fid = m['matchIDinofficial']
        home_team = Converter('zh-hans').convert(m['homeTeam']['teamName' + lang.upper()])
        away_team = Converter('zh-hans').convert(m['awayTeam']['teamName' + lang.upper()])
        match_time = datetime.strptime(m['matchTime'], "%Y-%m-%dT%H:%M:%S+08:00")
        odds = [float(m['hadodds']['H'].replace('100@', '')), float(m['hadodds']['D'].replace('100@', '')), float(m['hadodds']['A'].replace('100@', ''))]
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
    url = "http://nicpu1.cse.ust.hk:9001/lottery/betfair/sport/football"
    r = re.compile('<li class="com-coupon-line-new-layout layout-1 avb-row avb-table market-avb quarter-template market-2-columns">(.*?)ui-nav event-team-container ui-top event-link', re.MULTILINE | re.DOTALL)
    content = load_url(url)
    update = datetime.now()
    for m in r.finditer(content):
        rr = re.compile(r'market-3-runners(.*?)data-event="(.*?) v (.*?)"(.*?)<a href="/sport/football\?gaTab=(.*?)=&gaZone=Main&bseId=(.*?)&bsContext=REAL&bsmSt=(.*?)&bsUUID(.*?)ui-runner-price ui-(.*?) "> (.*?) </span> </a> </li>(.*?)ui-runner-price ui-(.*?) "> (.*?) </span> </a> </li>(.*?)ui-runner-price ui-(.*?) "> (.*?) </span> </a> </li>', re.MULTILINE | re.DOTALL)
        mm = rr.search(m.group(0))
        if mm is not None:
            try:
                fid = mm.group(6)
                home_team = mm.group(2)
                away_team = mm.group(3)
                match_time = datetime.fromtimestamp(float(mm.group(7)) / 1000)
                odds = [float(mm.group(10).strip()), float(mm.group(13).strip()), float(mm.group(16).strip())]
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
            return do_crawl(src)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def crawl(request):
    if "src" in request.GET:
        return do_crawl(request.GET["src"])
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def do_crawl(src):
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
