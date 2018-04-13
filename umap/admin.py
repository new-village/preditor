from django.contrib import admin

from umap.models import Result, Race, Prediction


class ResultInline(admin.TabularInline):
    model = Result
    fields = ("rank", "bracket", "horse_num", "horse_id", ("sex", "age"), "finish_time", "odds",
              "run_cnt", "t3r_horse", "t3r_jockey", "roi")
    readonly_fields = ("rank", "bracket", "horse_num", "horse_id", "sex", "age", "finish_time", "odds",
                       "run_cnt", "t3r_horse", "t3r_jockey", "roi")
    ordering = ["rank"]

    def has_delete_permission(self, request, obj):
        return False

    def has_add_permission(self, request):
        return False


class RaceAdmin(admin.ModelAdmin):
    list_display = ("race_dt", "place_name", "round", "title", "course", "weather", "condition",
                    "head_count", "max_prize", "odds_stdev", "result_flg")
    ordering = ["-result_flg", "-race_dt", "race_id"]
    search_fields = ["race_id", "race_dt"]
    inlines = [ResultInline]


class ResultAdmin(admin.ModelAdmin):
    list_display = ("rank", "bracket", "horse_num", "horse_id", "sex", "age", "finish_time", "odds", "odor")
    search_fields = ["key", "race__race_id"]


class PredictionAdmin(admin.ModelAdmin):
    list_display = ("label", "type", "recall", "precision", "note", "updated_at")


admin.site.register(Race, RaceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Prediction, PredictionAdmin)