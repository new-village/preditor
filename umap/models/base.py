import gzip
import pickle
import uuid

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
    type = models.CharField(max_length=16, null=True)                  # 芝（コース種別）
    length = models.IntegerField(null=True)                 # 2600（距離）
    weather = models.CharField(max_length=16, null=True)               # 晴 （天気）
    condition = models.CharField(max_length=16, null=True)             # 良（馬場状態）
    head_count = models.IntegerField(null=True)             # 16（頭数）
    max_prize = models.FloatField(null=True)                # 34000.0（優勝賞金）
    result_flg = models.BooleanField(default=False)

    def course(self):
        if self.type and self.length:
            course = str(self.type)+str(self.length)+"m"
        else:
            course = ""
        return course

    def _result_list(self):
        return [result for result in Result.objects.filter(race__race_id=self.race_id)]

    result_list = property(_result_list)

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
    time_lag = models.FloatField(null=True)                     # 0.1（1着との時間差）
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

    def __str__(self):
        return str(self.race_id)


class Pmodel(models.Model):
    class Meta:
        verbose_name = "予測モデル"
        verbose_name_plural = "予測モデル"

    title = models.CharField(primary_key=True, max_length=80)
    mbin = models.BinaryField(null=True)
    method = models.CharField(max_length=80)
    columns = models.TextField(null=True)
    recall = models.FloatField(null=True)
    precision = models.FloatField(null=True)
    roi = models.FloatField(null=True)
    note = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set(self, model):
        self.mbin = gzip.compress(pickle.dumps(model))

    def get(self):
        return pickle.loads(gzip.decompress(self.mbin))

    model_bin = property(get, set)

    def __str__(self):
        return str(self.title)


class Expect(models.Model):
    class Meta:
        verbose_name = "予測結果"
        verbose_name_plural = "予測結果"
        unique_together = ('result', 'pm_name')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=True)
    pm_name = models.CharField(max_length=80, null=True)
    clf_result = models.NullBooleanField()

    def __str__(self):
        return str(self.result)


class Log(models.Model):
    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "実行ログ"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField()
    pid = models.IntegerField()
    label = models.TextField(null=True)
    exec_time = models.DurationField(null=True)
    finish = models.BooleanField(default=False)

    def __str__(self):
        return str(self.result)