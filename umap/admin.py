from django.contrib import admin

from umap.models import Result, Race, Pmodel


class ResultInline(admin.TabularInline):
    flist = ["rank", "bracket", "horse_num", "horse_name", "sex", "age", "jockey_name", "weight", "finish_time",
                "time_lag", "odds", "prize", "clf1", "clf2"]
    model = Result
    fields = flist
    readonly_fields = flist
    ordering = ["rank", "horse_num"]

    def has_delete_permission(self, request, obj):
        return False

    def has_add_permission(self, request):
        return False


class RaceAdmin(admin.ModelAdmin):
    list_display = ("race_dt", "place_name", "round", "title", "course", "weather", "condition", "result_flg")
    ordering = ["-result_flg", "-race_dt", "race_id"]
    search_fields = ["race_id", "race_dt", "title", "results__horse_name", "place_name"]
    inlines = [ResultInline]


class ResultAdmin(admin.ModelAdmin):
    list_display = ("rank", "bracket", "horse_num", "horse_name", "sex", "age", "finish_time", "odds", "odor")
    search_fields = ["race__race_id", "race__title", "horse_name"]


class PmodelAdmin(admin.ModelAdmin):
    list_display = ("title", "method", "columns", "recall", "precision", "note", "updated_at")


admin.site.register(Race, RaceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Pmodel, PmodelAdmin)