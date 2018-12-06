import re
from datetime import date, datetime, timedelta
from time import sleep

import sys
from django.core.management import BaseCommand
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models import Min

from umap.models import Race, Result
from umap.uhelper import get_soup, str_now
from umap.uparser import insert_entry, was_created, update_race, insert_race

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
        # Set argument date if the args is available, or Set fore end date of this month
        from_dt = arg_parser(options["from"])

        # Get race list from SportsNavi
        for url in sportsnavi_urls(from_dt):
            page = get_soup(url)
            insert_race(page)
            sleep(5)

        # Get race result from Netkeiba.com
        base_url = "http://db.netkeiba.com/race/"
        for race in Race.objects.filter(race_dt__lt=latest, result_flg=False):
            get_netkeiba_data(base_url, race)
            sleep(5)

        # Get race entry from Netkeiba.com
        base_url = "http://race.netkeiba.com/?pid=race_old&id=c"
        if from_dt == latest:
            for race in Race.objects.filter(race_dt__gte=latest, result_flg=False):
                get_netkeiba_data(base_url, race)
                sleep(5)

        # Delete uncompleted data
        print(str_now() + " [DELETE]")
        Race.objects.filter(race_dt__lt=latest, result_flg=False).delete()
        Result.objects.filter(horse_num__isnull=True).delete()

        print(str_now() + " [FINISH]")
        sys.exit()


def sportsnavi_urls(start):
    # Set URL parameter
    end = None

    # Set TO date when execution with FROM option
    if start != latest:
        end = Race.objects.aggregate(Min('race_dt'))['race_dt__min']

    # Set To date When the undefining of FROM option or Initial execution of collector with FROM option
    if end is None:
        end = latest + timedelta(weeks=2)

    # Set variables
    base_url = "https://keiba.yahoo.co.jp/schedule/list/{YEAR}/?month={MONTH}"
    yr = re.compile("{YEAR}")
    mo = re.compile("{MONTH}")

    # Make URL by setting parameters
    urls = list()
    while start <= end:
        # CREATE URL
        url = yr.sub(start.strftime('%Y'), base_url)
        url = mo.sub(start.strftime('%m'), url)
        urls.append(url)
        start = start + relativedelta(months=+1, day=1)

    # Return list type url
    return urls


def get_netkeiba_data(_url, _race):
    page = get_soup(_url + _race.race_id)
    mode = was_created(page)
    if mode:
        insert_entry(page, _race)
        update_race(mode, page, _race)
        # TODO: ISSUES(#7) add payback


def arg_parser(_from):
    # Get option date
    if _from is not None:
        str_arg = _from[0]
        rtn_dt = date(int(str_arg[0:4]), int(str_arg[4:6]), 1)
    # Or fore end date from latest
    else:
        rtn_dt = latest

    return rtn_dt
