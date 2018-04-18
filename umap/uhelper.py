import re

from django.db.models import Avg
from requests import Session, HTTPError
import bs4 as bs

from umap.models import Result


def get_soup(url):
    try:
        session = Session()
        html = session.get(url)
        html.encoding = html.apparent_encoding
        soup = bs.BeautifulSoup(html.content, "html.parser", from_encoding=html.apparent_encoding)
    except HTTPError as e:
        print("HTTP error: {0}".format(e))
        raise
    return soup


def formatter(reg, target, type="char"):
    # Extract target variables
    fmt = re.compile(reg)
    val = fmt.findall(target)[0] if target is not None and fmt.search(target) else None

    # Redact comma from numerical values
    if type == "int" or type == "float":
        if val is None:
            val = 0
        else:
            val = re.sub(",", "", val)

    # Convert type
    if type == "int":
        value = int(val) if val is not None else 0
    elif type == "float":
        value = float(val) if val is not None else 0
    elif type == "char":
        value = str(val) if val is not None else ""
    else:
        value = None

    return value


def get_from_a(data, target="url"):
    if target == "url":
        value = data.a.get("href") if data.a is not None else None
    else:
        value = data.a.string if data.a is not None else None

    return value


def cal_jky_hist(jockey_id, race_dt):
    rtn = 0.0
    query = Result.objects.filter(jockey_id=jockey_id, race__result_flg=True, race__race_dt__lt=race_dt).exclude(rank=0).order_by("-race__race_dt")[:50]
    cnt = query.count()
    if cnt != 0:
        rtn = round(len([rec for rec in query if rec.rank <= 3]) / cnt, 3)
    return rtn


def cal_hrs_hist(horse_id, race_dt):
    rtn = {"cnt_run": 0, "t3r_horse": 0.0, "avg_ror": 0.0, "avg_prize": 0.0, "avg_last3f": 0.0}
    query = Result.objects.filter(horse_id=horse_id, race__result_flg=True, race__race_dt__lt=race_dt).exclude(rank=0).order_by("-race__race_dt")
    cnt = query.count()

    last5 = query[:5]
    l5_cnt = query[:5].count()

    if l5_cnt != 0:
        top3 = [rec.odds for rec in last5 if rec.rank <= 3]
        rtn["cnt_run"] = cnt
        rtn["t3r_horse"] = round(len(top3) / l5_cnt, 3)
        rtn["avg_ror"] = round(sum(top3) / l5_cnt, 3)
        rtn["avg_prize"] = round(sum([rec.prize for rec in last5]) / l5_cnt, 3)
        rtn["avg_last3f"] = round(sum([rec.last3f_time for rec in last5]) / l5_cnt, 3)
    return rtn
