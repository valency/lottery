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
        for m in r.finditer(content):
            fid = m.group(2)
            home_team = m.group(3)
            away_team = m.group(4)
            match_time = m.group(6).replace("开赛时间：", "")
            odds = [m.group(9), m.group(11), m.group(13)]
            print fid, home_team, away_team, match_time, odds


Lottery500.list()
