import re
from datetime import date, datetime

from requests import Session, HTTPError
import bs4 as bs


def get_soup(_url):
    print(str_now() + " [GET] " + _url)
    try:
        session = Session()
        html = session.get(_url)
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


def fore_end(_date):
    year = _date.year
    month = _date.month
    return date(year, month, 1)


def str_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
