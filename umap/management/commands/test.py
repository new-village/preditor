import pandas as pd
from datetime import timedelta
from tqdm._tqdm_notebook import tqdm_notebook


def calc_rate(hid, rdt, mpz):
    from_dt = rdt - timedelta(weeks=53)
    query = Result.objects.filter(horse_id=hid, race__race_dt__gte=from_dt, race__result_flg=True).exclude(
        rank=0).exclude(race__type="障害").values("prize")
    pz_list = [q.prize / mpz for q in query]
    avg_rate = sum(pz_list) / len(pz_list)
    max_rate = max(pz_list)

    return pd.Series([avg_rate, max_rate])


tqdm_notebook.pandas()
df[["hrs_avg_rate", "hrs_max_rate"]] = df.progress_apply(
    lambda row: calc_rate(row["horse_id"], row["race_dt"], row["max_prize"]), axis=1)
df.head()