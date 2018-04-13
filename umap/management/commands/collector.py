import re
from datetime import date, datetime, timedelta
from time import sleep

import sys
from django.core.management import BaseCommand
from dateutil.relativedelta import relativedelta
from django.db.models import Min

from umap.models import Race, Result
from umap.uhelper import get_soup
from umap.uparser import insert_race, insert_entry, update_race, update_race_entry, was_existed, enrich_data

latest = datetime.now().date() - timedelta(days=3)


class Command(BaseCommand):
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument(
            '--from',
            dest='from',
            nargs=1,
            metavar="YYYYMMDD",
            help='You can set collection start date. format by YYYYMMDD.',
        )

    def handle(self, *args, **options):
        option = options["from"]
        # Get race schedule
        for url in sportsnavi_urls(option):
            soup = get_soup(url)
            insert_race(soup)

        # Get result & entry data
        if option:
            collect_data("result")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [ENRICH]")
            for result in Result.objects.all():
                enrich_data(result)
        else:
            for mode in ["result", "entry"]:
                collect_data(mode)

        # Delete uncompleted data
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [DELETE]")
        Race.objects.filter(race_dt__lt=latest, result_flg=False).delete()

        sys.exit()


def sportsnavi_urls(option):
    # Set URL parameter
    start_date = latest
    end_date = start_date + relativedelta(months=+1, day=1)

    # Override URL parameter, if command is had argument.
    if option:
        string_date = option[0]
        start_date = date(int(string_date[0:4]), int(string_date[4:6]), 1)
        end_date = Race.objects.aggregate(Min('race_dt'))['race_dt__min']

    # Set variables
    base_url = "https://keiba.yahoo.co.jp/schedule/list/{YEAR}/?month={MONTH}"
    yr = re.compile("{YEAR}")
    mo = re.compile("{MONTH}")

    # Make URL by setting parameters
    urls = list()
    while start_date <= end_date:
        # CREATE URL
        url = yr.sub(start_date.strftime('%Y'), base_url)
        url = mo.sub(start_date.strftime('%m'), url)
        urls.append(url)
        start_date = start_date + relativedelta(months=+1, day=1)

    # Return list type url
    return urls


def netkeiba_urls(mode="result"):
    urls = list()

    if mode == "result":
        # Get race_id whose result flag is FALSE
        races = Race.objects.filter(race_dt__lt=latest, result_flg=False).values("race_id")
        base_url = "http://db.netkeiba.com/race/"
    if mode == "entry":
        # Get race_id whose result flag is FALSE
        races = Race.objects.filter(race_dt__gte=latest, result_flg=False).values("race_id")
        base_url = "http://race.netkeiba.com/?pid=race_old&id=c"

    # Make URL by race_ids
    for race in races:
        urls.append(base_url + race["race_id"])

    return urls


def collect_data(mode):
    for url in netkeiba_urls(mode):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [GET] " + url)
        soup = get_soup(url)
        race = was_existed(soup)
        if race:
            insert_entry(soup, race)
            if mode == "entry":
                update_race_entry(soup, race)
            else:
                update_race(soup, race)
