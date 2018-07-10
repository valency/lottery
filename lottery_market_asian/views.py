# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lottery.common import *


@api_view(['GET'])
def macau_slot(request):
    url = "http://nicpu1.cse.ust.hk/lottery/macauslot/soccer/xml/odds/odds_config.xml?nocache=" + str(datetime.now())
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
    odds = load_xml("http://nicpu1.cse.ust.hk/lottery/macauslot/soccer/xml/odds/winodds.xml?nocache=" + str(datetime.now()))
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
    return Response(status=status.HTTP_201_CREATED)
