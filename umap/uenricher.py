from django.db import transaction
from django.db.models import Max, StdDev

from umap.models import Result
from umap.uhelper import str_now


@transaction.atomic
def enrich_data(_races):
    for race in _races:
        print(str_now() + " [ENRICH] " + race.race_id)
        enrich_race(race)
        enrich_results(race.result_list)
    return


def enrich_race(_race):
    _race.head_count = _race.results.exclude(rank=0).count()
    _race.max_prize = _race.results.exclude(rank=0).aggregate(Max("prize"))["prize__max"]
    _race.odds_stdev = round(_race.results.exclude(rank=0).aggregate(StdDev("odds"))["odds__stddev"], 3)
    _race.save()
    return


def enrich_results(_results):
    for result in _results:
        result.t3r_jockey = cal_jky_hist(result.jockey_id, result.race.race_dt)

        hrs_hist = cal_hrs_hist(result.horse_id, result.race.race_dt)
        result.cnt_run = hrs_hist["cnt_run"]
        result.t3r_horse = hrs_hist["t3r_horse"]
        result.avg_ror = hrs_hist["avg_ror"]
        result.avg_prize = hrs_hist["avg_prize"]
        result.avg_last3f = hrs_hist["avg_last3f"]
        result.save()
    return


def cal_jky_hist(jockey_id, race_dt):
    rtn = 0.0
    query = Result.objects.filter(jockey_id=jockey_id, race__result_flg=True, race__race_dt__lt=race_dt).exclude(rank=0, rank__isnull=True).order_by("-race__race_dt")[:50]
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
