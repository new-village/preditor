import re
import bs4
from datetime import date

from django.db import transaction
from django.db.models import Max, Count

from umap.models import Race, Result
from umap.uhelper import formatter, get_from_a


@transaction.atomic
def insert_race(soup):
    # Extract year and month field
    year_month = soup.find("h3", {"class": "midashi3rd"}).string
    year = formatter("(\d+)年\d+月", year_month, "int")
    month = formatter("\d+年(\d+)月", year_month, "int")

    for row in soup.select("tbody tr"):
        cells = row.findAll('td')

        if len(cells) > 2 and cells[0].find("a") is not None:
            race_id_without_round = "20" + formatter("\d+", get_from_a(cells[0]))
            day = formatter("(\d+)日（[日月火水木金土]）", str(cells[0]), "int")
            place_id = race_id_without_round[4:6]
            place_name = to_place_name(place_id)
            days = int(race_id_without_round[6:8])
            times = int(race_id_without_round[8:10])

            for r in range(1, 13):
                Race.objects.get_or_create(
                    race_id=race_id_without_round + str(r).zfill(2),
                    race_dt=date(year, month, day),
                    place_id=place_id,
                    place_name=place_name,
                    days=days,
                    times=times,
                    round=r
                )
    return


def update_race(_mode, _page, _race):
    if _mode == "result":
        update_race_result(_page, _race)
    elif _mode == "entry":
        update_race_entry(_page, _race)
    return


def update_race_result(soup, race):
    race.title = soup.find("title").string.split(u"｜")[0]
    race.grade = formatter("\((G\d)\)", str(soup.find("dl", {"class": "racedata"}).find("h1")))

    # RACE DETAILS
    line = soup.find("dl", attrs={"class": "racedata"}).find("span").string.split(u"\xa0/\xa0")
    race.type = to_course_full(formatter("[芝ダ障]", line[0]))
    race.length = formatter("\d{4}", line[0], "int")
    race.weather = formatter("晴|曇|小雨|雨|小雪|雪", line[1])
    race.condition = formatter("良|稍重|重|不良", line[2])

    # RACE SUMMARY INFORMATION
    race.head_count, race.max_prize = agg_results(race)

    race.result_flg = True
    race.save()
    return


def update_race_entry(soup, race):
    # Parse HTML
    racedata = soup.find("dl", {"class": "racedata"}).find("dd")
    course = racedata.find_all("p")[0].string
    conditions = racedata.find_all("p")[1].string.split(u"\xa0/\xa0")
    otherdata = soup.find("div", {"class": "race_otherdata"}).findAll('p')

    race.title = formatter("\w+", str(racedata.find('h1').string))
    race.type = to_course_full(formatter("[芝ダ障]", course))
    race.length = formatter("\d{4}", course, "int")
    race.weather = formatter("晴|曇|小雨|雨|小雪|雪", conditions[1])
    race.condition = formatter("良|稍重|重|不良", conditions[2])
    race.head_count = formatter("\d+", otherdata[1].string, "int")
    race.max_prize = formatter("\d+", otherdata[2].string, "int")

    race.save()
    return


@transaction.atomic
def insert_entry(soup, race):
    # Extract Entry or Result Table
    table = soup.find("table",  {"class": ["race_table_old", "race_table_01"]})

    # Create dummy table for avoiding loop error.
    if table is None:
        table = bs4.BeautifulSoup("<tr><td></td></tr>", "html.parser")

    time_of_first = 0

    # Delete exist data
    Result.objects.filter(race=race).delete()

    for row in table.findAll("tr"):
        cells = row.findAll("td")

        # IF the table is not listed all information, abort parse.

        if len(cells) == 21:
            result = parse_result(cells, race, time_of_first)
        elif len(cells) == 13:
            result = parse_entry_13(cells, race)
        elif len(cells) == 12:
            result = parse_entry_12(cells, race)
        elif len(cells) == 10:
            result = parse_entry_10(cells, race)
        elif len(cells) == 8:
            result = parse_entry_8(cells, race)

        if 'result' in locals():
            result.save()

            if result.rank == 1:
                time_of_first = result.finish_time

    return


def parse_result(cells, race, tof):
    result = Result()

    result.race = race
    result.rank = formatter("\d+", cells[0].string, "int")
    result.bracket = formatter("\d+", cells[1].string, "int")
    result.horse_num = formatter("\d+", cells[2].string, "int")
    result.horse_id = formatter("\d+", get_from_a(cells[3]))
    result.horse_name = formatter("[^!-~\xa0]+", get_from_a(cells[3], "name"))
    result.key = race.race_id + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[4].string)
    result.age = formatter("\d+", cells[4].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[5].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[6]))
    result.jockey_name = formatter("[^!-~\xa0]+", get_from_a(cells[6], "name"))

    if cells[7].string is not None:
        tmp_time = re.split(r"[:.]", cells[7].string)
        tmp_time = [int(i) for i in tmp_time]  # Type conversion
        tmp_sec = (tmp_time[0] * 60 + tmp_time[1]) + (tmp_time[2] / 10)
        result.finish_time = tmp_sec
    result.time_lag = round(result.finish_time - tof, 2) if result.finish_time is not None and tof != 0 else 0

    result.last3f_time = formatter("\d+.\d+", cells[11].string, "float")
    result.odds = formatter("\d+.\d+", cells[12].string, "float")
    result.odor = formatter("\d+", cells[13].string, "int")
    result.weight = formatter("(\d+)\([+-]?\d*\)", cells[14].string, "int")
    result.weight_diff = formatter("\d+\(([+-]?\d+)\)", cells[14].string, "int")
    result.trainer_id = formatter("\d+", get_from_a(cells[15]))
    result.trainer_name = formatter("[^!-~\xa0]+", get_from_a(cells[15], "name"))
    result.owner_id = formatter("\d+", get_from_a(cells[19]))
    result.owner_name = formatter("[^!-~\xa0]+", get_from_a(cells[19], "name"))
    result.prize = formatter("\d*,?\d*.?\d+", cells[20].string, "float")

    return result


def parse_entry_13(cells, race):
    result = Result()

    result.race = race
    result.bracket = formatter("\d+", cells[0].string, "int")
    result.horse_num = formatter("\d+", cells[1].string, "int")
    result.horse_id = formatter("\d+", get_from_a(cells[3]))
    result.horse_name = formatter("[^!-~\xa0]+", get_from_a(cells[3], "name"))
    result.key = race.race_id + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[4].string)
    result.age = formatter("\d+", cells[4].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[5].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[6]))
    result.jockey_name = formatter("[^!-~\xa0]+", get_from_a(cells[6], "name"))
    result.trainer_id = formatter("\d+", get_from_a(cells[7]))
    result.trainer_name = formatter("[^!-~\xa0]+", get_from_a(cells[7], "name"))
    result.weight = formatter("(\d+)\([+-]?\d*\)", cells[8].string, "int")
    result.weight_diff = formatter("\d+\(([+-]?\d+)\)", cells[8].string, "int")
    result.odds = formatter("\d+.\d+", cells[9].string, "float")
    result.odor = formatter("\d+", cells[10].string, "int")

    return result


def parse_entry_12(cells, race):
    result = Result()

    result.race = race
    result.bracket = formatter("\d+", cells[0].string, "int")
    result.horse_num = formatter("\d+", cells[1].string, "int")
    result.horse_id = formatter("\d+", get_from_a(cells[3]))
    result.horse_name = formatter("[^!-~\xa0]+", get_from_a(cells[3], "name"))
    result.key = race.race_id + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[4].string)
    result.age = formatter("\d+", cells[4].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[5].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[6]))
    result.jockey_name = formatter("[^!-~\xa0]+", get_from_a(cells[6], "name"))
    result.trainer_id = formatter("\d+", get_from_a(cells[7]))
    result.trainer_name = formatter("[^!-~\xa0]+", get_from_a(cells[7], "name"))
    result.odds = formatter("\d+.\d+", cells[8].string, "float")
    result.odor = formatter("\d+", cells[9].string, "int")

    return result


def parse_entry_10(cells, race):
    result = Result()

    result.race = race
    result.horse_id = formatter("\d+", get_from_a(cells[1]))
    result.horse_name = formatter("[^!-~\xa0]+", get_from_a(cells[1], "name"))
    result.key = race.race_id + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[2].string)
    result.age = formatter("\d+", cells[2].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[3].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[4]))
    result.jockey_name = formatter("[^!-~\xa0]+", get_from_a(cells[4], "name"))
    result.trainer_id = formatter("\d+", get_from_a(cells[5]))
    result.trainer_name = formatter("[^!-~\xa0]+", get_from_a(cells[5], "name"))
    result.odds = formatter("\d+.\d+", cells[6].string, "float")
    result.odor = formatter("\d+", cells[7].string, "int")

    return result


def parse_entry_8(cells, race):
    result = Result()

    result.race = race
    result.horse_id = formatter("\d+", get_from_a(cells[1]))
    result.horse_name = formatter("[^!-~\xa0]+", get_from_a(cells[1], "name"))
    result.key = race.race_id + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[2].string)
    result.age = formatter("\d+", cells[2].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[3].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[4]))
    result.jockey_name = formatter("[^!-~\xa0]+", get_from_a(cells[4], "name"))
    result.trainer_id = formatter("\d+", get_from_a(cells[5]))
    result.trainer_name = formatter("[^!-~\xa0]+", get_from_a(cells[5], "name"))
    result.odds = 0
    result.odor = 0

    return result


def was_created(soup):
    # What kind of soup?
    val = soup.find("title").string
    if re.search("\d+/\d+/\d+", val) is not None:
        rtn_code = "entry"
    elif re.search("\d+年\d+月\d+日", val) is not None:
        rtn_code = "result"
    else:
        rtn_code = None

    # When the table is not exist on entry page, set abort process flag
    if len(soup.findAll("table",  {"class": ["race_table_old", "race_table_01"]})) == 0:
        rtn_code = None

    return rtn_code


def to_place_name(place_id):
    master = {"01": "札幌", "02": "函館", "03": "福島", "04": "新潟", "05": "東京", "06": "中山", "07": "中京",
              "08": "京都", "09": "阪神", "10": "小倉"}
    place_name = master[place_id]
    return place_name


def to_course_full(abbr):
    master = {"ダ": "ダート", "障": "障害", "芝": "芝"}
    course_full = master[abbr] if abbr is not '' else 0
    return course_full


def agg_results(_race):
    query = Result.objects.filter(race__race_id=_race.race_id).exclude(rank=0).aggregate(Max("prize"), Count("key"))
    head_count = round(query["key__count"], 2) if query["key__count"] is not None else 0
    max_prize = round(query["prize__max"], 2) if query["prize__max"] is not None else 0

    return [head_count, max_prize]
