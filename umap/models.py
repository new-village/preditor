from django.db import models


class Race(models.Model):
    class Meta:
        verbose_name = "レース"
        verbose_name_plural = "レース"
        indexes = [
            models.Index(fields=["race_dt"]),
        ]

    race_id = models.CharField(primary_key=True, max_length=12)
    race_dt = models.DateField(null=True, db_index=True)    # 2017-12-28（開催日）
    place_id = models.CharField(max_length=2)               # 06（場所ID）
    place_name = models.CharField(max_length=8)             # 中山（場所名）
    days = models.IntegerField(null=True)                   # 9（日数）
    times = models.IntegerField(null=True)                  # 5（回数）
    round = models.IntegerField(null=True)                  # 11（ラウンド）
    title = models.CharField(max_length=80)                 # ホープフルステークス（レース名）
    grade = models.CharField(max_length=2, null=True)       # G1（グレード）
    type = models.CharField(max_length=16)                  # 芝（コース種別）
    length = models.IntegerField(null=True)                 # 2600（距離）
    weather = models.CharField(max_length=16)               # 晴 （天気）
    condition = models.CharField(max_length=16)             # 良（馬場状態）
    head_count = models.IntegerField(null=True)             # 16（頭数）
    max_prize = models.FloatField(null=True)                # 34000.0（優勝賞金）
    odds_stdev = models.FloatField(null=True)               # 15.3（オッズ標準偏差）
    result_flg = models.BooleanField(default=False)

    def course(self):
        if self.type and self.length:
            course = str(self.type)+str(self.length)+"m"
        else:
            course = ""

        return course

    def __str__(self):
        return str(self.times)+"回"+str(self.place_name)+str(self.days)+"日目 "+str(self.round)+"R"


class Result(models.Model):
    class Meta:
        verbose_name = "出走情報"
        verbose_name_plural = "出走情報"
        indexes = [
            models.Index(fields=["horse_id"]),
            models.Index(fields=["jockey_id"]),
        ]

    key = models.CharField(primary_key=True, max_length=34)
    race = models.ForeignKey(Race, related_name="results", on_delete=models.CASCADE)
    rank = models.IntegerField(null=True)                       # 1（着順）
    bracket = models.IntegerField(null=True)                    # 1（枠番）
    horse_num = models.IntegerField(null=True)                  # 2（馬番）
    horse_id = models.CharField(max_length=12, db_index=True)   # 2012102013（馬ID）
    horse_name = models.CharField(max_length=80)                # キタサンブラック（馬名）
    sex = models.CharField(max_length=4)                        # 牡（性別）
    age = models.IntegerField(null=True)                        # 5（年齢）
    burden = models.FloatField(null=True)                       # 57（斤量）
    jockey_id = models.CharField(max_length=10)                 # 00666（騎手ID）
    jockey_name = models.CharField(max_length=80)               # 武豊（騎手名）
    finish_time = models.FloatField(null=True)                  # 153.6（タイム）
    last3f_time = models.FloatField(null=True)                  # 34.6（上がり）
    odds = models.FloatField(null=True)                         # 4.7（オッズ）
    odor = models.IntegerField(null=True)                       # 2（人気順）
    weight = models.IntegerField(null=True)                     # 540（馬体重）
    weight_diff = models.IntegerField(null=True)                # -2（体重差）
    trainer_id = models.CharField(max_length=10)                # 01110（調教師）
    trainer_name = models.CharField(max_length=80)              # 01110（調教師名）
    owner_id = models.CharField(max_length=12)                  # 01110（馬主）
    owner_name = models.CharField(max_length=80)                # 01110（馬主）
    prize = models.FloatField(null=True)                        # 3000.12（賞金）
    t3r_jockey = models.FloatField(null=True)                   # 騎手複勝率（直近10走）
    cnt_run = models.IntegerField(null=True)                    # 出走回数
    t3r_horse = models.FloatField(null=True)                    # 競走馬複勝率（直近5走）
    avg_ror = models.FloatField(null=True)                      # 平均回収率（直近5走）
    avg_prize = models.FloatField(null=True)                    # 平均獲得賞金（直近5走）
    avg_last3f = models.FloatField(null=True)                   # 平均上り3Fタイム（直近5走）
    clf_result = models.NullBooleanField()                      # 予想結果（分類）
    clf_result2 = models.IntegerField(null=True)                # 予想結果（分類）
    reg_result = models.FloatField(null=True)                   # 予想結果（回帰）
    reg_result2 = models.FloatField(null=True)                  # 予想結果（回帰）

    def __str__(self):
        return str(self.race_id)


class Prediction(models.Model):
    class Meta:
        verbose_name = "予測モデル"
        verbose_name_plural = "予測モデル"

    label = models.CharField(primary_key=True, max_length=80)
    trained = models.BinaryField(null=False)
    target = models.CharField(max_length=80)
    recall = models.FloatField(null=False)
    precision = models.FloatField(null=False)
    note = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.label)