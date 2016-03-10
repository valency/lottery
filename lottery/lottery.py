# -*- coding: utf-8 -*-

import re

from common import *


class Lottery500:
    def __init__(self):
        pass

    @staticmethod
    def list():
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
        return games


class MacauSlot:
    def __init__(self):
        pass

    @staticmethod
    def list():
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
        return games
