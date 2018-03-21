from datetime import date

from django.db import transaction

from umap.models import Race
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
                race = Race()

                race.race_id = race_id_without_round + str(r).zfill(2)
                race.race_dt = date(year, month, day)
                race.place_id = place_id
                race.place_name = place_name
                race.days = days
                race.times = times
                race.round = r
                race.save()
    return


def to_place_name(place_id):
    master = {"01": "札幌", "02": "函館", "03": "福島", "04": "新潟", "05": "東京", "06": "中山", "07": "中京",
              "08": "京都", "09": "阪神", "10": "小倉"}
    place_name = master[place_id]
    return place_name
