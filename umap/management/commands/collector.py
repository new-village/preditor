import re
from datetime import date, datetime, timedelta

from django.core.management import BaseCommand
from dateutil.relativedelta import relativedelta
from django.db.models import Min

from umap.models import Race
from umap.uhelper import get_soup
from umap.uparser import insert_race

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
        for url in sportsnavi_urls(option):
            soup = get_soup(url)
            insert_race(soup)


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
