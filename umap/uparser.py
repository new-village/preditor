import re
import statistics
import bs4
from datetime import date

from django.db import transaction
from django.db.models import Count, Max, Avg

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


def update_race(soup, race):
    race.title = soup.find("title").string.split(u"｜")[0]
    race.grade = formatter("\((G\d)\)", str(soup.find("dl", {"class": "racedata"}).find("h1")))

    # RACE DETAILS
    line = soup.find("dl", attrs={"class": "racedata"}).find("span").string.split(u"\xa0/\xa0")
    race.type = to_course_full(formatter("[芝ダ障]", line[0]))
    race.length = formatter("\d+", line[0], "int")
    race.weather = line[1].split(" : ")[1]

    # CONDITION
    condition = line[2].split(" : ")[1]
    if re.search("  ", condition):
        race.condition = condition.split("  ")[0]
    else:
        race.condition = condition

    race.head_count = race.results.aggregate(Count("rank"))["rank__count"]
    race.max_prize = race.results.aggregate(Max("prize"))["prize__max"]
    race.odds_stdev = round(statistics.pstdev(race.results.exclude(rank=0).values_list('odds', flat=True)), 2)

    race.result_flg = True
    race.save()

    return


def update_race_entry(soup, race):
    # Parse HTML
    racedata = soup.find("dl", {"class": "racedata"}).find("dd")
    conditions = racedata.find("span").string.split(u"\xa0/\xa0")
    otherdata = soup.find("div", {"class": "race_otherdata"}).findAll('p')

    race.title = formatter("[^!-~\xa0]+", str(racedata.find('h1')))
    race.type = to_course_full(formatter("[芝ダ障]", conditions[0]))
    race.length = formatter("\d+", conditions[0], "int")
    race.weather = formatter("(晴|曇|小雨|雨|小雪|雪)", conditions[1])
    race.condition = formatter("(良|稍重|重|不良)", conditions[2])
    race.head_count = formatter("\d+", otherdata[1].string, "int")
    race.max_prize = formatter("\d+", otherdata[2].string, "int")
    # Error avoidance logic: When the len(cells) equal 8, rise statistics error.
    try:
        race.odds_stdev = round(statistics.pstdev(race.results.values_list('odds', flat=True)), 2)
    except statistics.StatisticsError:
        pass

    race.save()
    return


@transaction.atomic
def insert_entry(soup, race):
    # Extract Entry or Result Table
    table = soup.findAll("table",  {"class": ["race_table_old", "race_table_01"]})

    if len(table) == 1:
        table = table[0]
    else:
        table = bs4.BeautifulSoup("<tr><td></td></tr>", "html.parser")

    for row in table.findAll("tr"):
        cells = row.findAll("td")
        #print(len(cells))

        # IF the table is not listed all information, abort parse.
        if len(cells) == 21:
            result = parse_result(cells, race)
        elif len(cells) == 13:
            result = parse_entry_13(cells, race)
        elif len(cells) == 10:
            result = parse_entry_10(cells, race)
        elif len(cells) == 8:
            result = parse_entry_8(cells, race)

        if 'result' in globals():
            result.save()

    return


def parse_result(cells, race):
    result = Result()

    result.race = race
    result.rank = formatter("\d+", cells[0].string, "int")
    result.bracket = formatter("\d+", cells[1].string, "int")
    result.horse_num = formatter("\d+", cells[2].string, "int")
    result.horse_id = formatter("\d+", get_from_a(cells[3]))
    result.key = str(race) + "-" + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[4].string)
    result.age = formatter("\d+", cells[4].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[5].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[6]))

    if cells[7].string is not None:
        tmp_time = re.split(r"[:.]", cells[7].string)
        tmp_time = [int(i) for i in tmp_time]  # Type conversion
        tmp_sec = (tmp_time[0] * 60 + tmp_time[1]) + (tmp_time[2] / 10)
        result.finish_time = tmp_sec

    result.last3f_time = formatter("\d+.\d+", cells[11].string, "float")
    result.odds = formatter("\d+.\d+", cells[12].string, "float")
    result.odor = formatter("\d+", cells[13].string, "int")
    result.weight = formatter("(\d+)\([+-]?\d*\)", cells[14].string, "int")
    result.weight_diff = formatter("\d+\(([+-]?\d+)\)", cells[14].string, "int")
    result.trainer_id = formatter("\d+", get_from_a(cells[15]))
    result.owner_id = formatter("\d+", get_from_a(cells[19]))
    result.prize = formatter("\d*,?\d*.?\d+", cells[20].string, "float")

    return result


def parse_entry_13(cells, race):
    result = Result()

    result.race = race
    result.bracket = formatter("\d+", cells[0].string, "int")
    result.horse_num = formatter("\d+", cells[1].string, "int")
    result.horse_id = formatter("\d+", get_from_a(cells[3]))
    result.key = str(race) + "-" + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[4].string)
    result.age = formatter("\d+", cells[4].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[5].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[6]))
    result.trainer_id = formatter("\d+", get_from_a(cells[7]))
    result.weight = formatter("(\d+)\([+-]?\d*\)", cells[8].string, "int")
    result.weight_diff = formatter("\d+\(([+-]?\d+)\)", cells[8].string, "int")
    result.odds = formatter("\d+.\d+", cells[9].string, "float")
    result.odor = formatter("\d+", cells[10].string, "int")

    return result


def parse_entry_10(cells, race):
    result = Result()

    result.race = race
    result.horse_id = formatter("\d+", get_from_a(cells[1]))
    result.key = str(race) + "-" + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[2].string)
    result.age = formatter("\d+", cells[2].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[3].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[4]))
    result.trainer_id = formatter("\d+", get_from_a(cells[5]))
    result.odds = formatter("\d+.\d+", cells[6].string, "float")
    result.odor = formatter("\d+", cells[7].string, "int")

    return result


def parse_entry_8(cells, race):
    result = Result()

    result.race = race
    result.horse_id = formatter("\d+", get_from_a(cells[1]))
    result.key = str(race) + "-" + result.horse_id
    result.sex = formatter("[牡牝騸セ]", cells[2].string)
    result.age = formatter("\d+", cells[2].string, "int")
    result.burden = formatter("(\d+).?\d?", cells[3].string, "float")
    result.jockey_id = formatter("\d+", get_from_a(cells[4]))
    result.trainer_id = formatter("\d+", get_from_a(cells[5]))

    return result


def was_existed(soup):
    fmt = re.compile("(\d+/\d+/\d+|\d+年\d+月\d+日)")
    val = soup.find("title").string

    if fmt.search(val) is not None:
        race_id = formatter("\d+", soup.find("li", {"class": ["race_navi_result", "race_navi_shutuba"]}).a.get("href"))
        race = Race.objects.get(pk=race_id)
    else:
        race = None

    # When the table is not exist on entry page, set abort process flag
    if len(soup.findAll("table",  {"class": ["race_table_old", "race_table_01"]})) == 0:
        race = None

    return race


def to_place_name(place_id):
    master = {"01": "札幌", "02": "函館", "03": "福島", "04": "新潟", "05": "東京", "06": "中山", "07": "中京",
              "08": "京都", "09": "阪神", "10": "小倉"}
    place_name = master[place_id]
    return place_name


def to_course_full(abbr):
    master = {"ダ": "ダート", "障": "障害", "芝": "芝"}
    course_full = master[abbr]
    return course_full
