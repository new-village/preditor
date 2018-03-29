import sys
from datetime import datetime, timedelta
from time import sleep

from django.core.management import BaseCommand

from umap.models import Race
from umap.uhelper import get_soup
from umap.uparser import was_done, insert_entry, update_race_entry


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        # Get race schedule
        for url in entry_urls():
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [GET] " + url)
            soup = get_soup(url)
            race = was_done(soup)
            if race:
                insert_entry(soup, race)
                update_race_entry(soup, race)
            sleep(3)

        sys.exit()


def entry_urls():
    urls = list()

    # Get race_id whose result flag is FALSE
    latest = datetime.now().date() + timedelta(days=5)
    races = Race.objects.filter(race_dt__lt=latest, result_flg=False).values("race_id")

    # Make URL by race_ids
    base_url = "http://race.netkeiba.com/?pid=race_old&id=c"
    for race in races:
        urls.append(base_url + race["race_id"])

    return urls

