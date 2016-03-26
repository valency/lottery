# -*- coding: utf-8 -*-

import re
from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lib.langconv import *
from lottery.common import *
from serializers import *


@api_view(['GET'])
def list_lottery_500(request):
    url = "http://trade.500.com/jczq/"
    content = load_url(url, "GBK")
    r = re.compile(r"<tr zid=(.*?)fid=\"(.*?)\" homesxname=\"(.*?)\" awaysxname=\"(.*?)\"(.*?)class=\"match_time\" title=\"(.*?)\"(.*?)<div class=\"bet_odds\">(.*?)data-sp=\"(.*?)\"(.*?)data-sp=\"(.*?)\"(.*?)data-sp=\"(.*?)\"(.*?)</div>(.*?)</tr>", re.MULTILINE | re.DOTALL)
    games = []
    for m in r.finditer(content):
        fid = m.group(2)
        home_team = m.group(3).replace("  ", "")
        away_team = m.group(4).replace("  ", "")
        match_time = m.group(6).replace("开赛时间：", "")
        odds = [m.group(9), m.group(11), m.group(13)]
        games.append({
            "id": fid,
            "home": home_team,
            "away": away_team,
            "t": match_time,
            "odds": {
                "home": odds[0],
                "draw": odds[1],
                "away": odds[2]
            }
        })
    return Response(games)


@api_view(['GET'])
def list_hkjc(request):
    url = "http://bet.hkjc.com/football/index.aspx"
    content = load_url(url)
    r = re.compile(r"rmid(.*?)\">(.*?)title=\"對賽往績\">(.*?) <label class='lblvs'>對</label> (.*?)</a></span></td>(.*?)<td class=\"cesst ttgR2\"><span>(.*?)</span></td>(.*?)HAD_H\">(.*?)</span></a></span></td>(.*?)HAD_D\">(.*?)</span></a></span></td>(.*?)HAD_A\">(.*?)</span></a></span></td>")
    games = []
    for m in r.finditer(content):
        fid = m.group(1)
        home_team = Converter('zh-hans').convert(m.group(3).decode('utf-8')).encode('utf-8')
        away_team = Converter('zh-hans').convert(m.group(4).decode('utf-8')).encode('utf-8')
        match_time = str(date.today().year) + "-" + m.group(6)[3:5] + "-" + m.group(6)[:2] + m.group(6)[5:]
        odds = [m.group(8), m.group(10), m.group(12)]
        games.append({
            "id": fid,
            "home": home_team,
            "away": away_team,
            "t": match_time,
            "odds": {
                "home": odds[0],
                "draw": odds[1],
                "away": odds[2]
            }
        })
    return Response(games)


@api_view(['GET'])
def list_macau_slot(request):
    url = "http://web.macauslot.com/soccer/xml/odds/odds_config.xml?nocache=" + str(datetime.now())
    configs = load_xml(url)
    games = []
    for config in configs.findall("Fixture"):
        t = config.attrib["gt"]
        t = string_insert(t, "-", 4)
        t = string_insert(t, "-", 7)
        games.append({
            "id": config.attrib["id"],
            "home": config.attrib["sh"],
            "away": config.attrib["sa"],
            "t": t
        })
    odds = load_xml("http://web.macauslot.com/soccer/xml/odds/winodds.xml?nocache=" + str(datetime.now()))
    for odd in odds.findall("Fixture"):
        game_index = dict_search(games, "id", odd.attrib["id"])
        if game_index is not None:
            game = games[game_index]
            game["odds"] = [{
                "team": odd.attrib["g"],
                "mode": odd.attrib["gg"],
                "home": odd.attrib["ho"],
                "away": odd.attrib["ao"]
            }]
            if "var" in odd.attrib:
                var = odd.attrib["var"].split(",")
                for i in range(0, len(var), 5):
                    game["odds"].append({
                        "team": var[i],
                        "mode": var[i + 1],
                        "home": var[i + 2],
                        "away": var[i + 3]
                    })
    return Response(games)


@api_view(['GET'])
def list_alias(request):
    return Response(AliasSerializer(Alias.objects.all(), many=True).data)


@api_view(['GET'])
def add_alias(request):
    if "a" in request.GET and "b" in request.GET:
        try:
            Alias.objects.get(a=request.GET["a"], b=request.GET["b"])
            return Response(status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            alias = Alias(a=request.GET["a"], b=request.GET["b"])
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
