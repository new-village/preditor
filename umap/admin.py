from django.contrib import admin

from umap.models import Result, Race, Pmodel, Log


class ResultInline(admin.TabularInline):
    fields = ["rank", "bracket", "horse_num", "horse_name", "sex", "age", "jockey_name", "weight", "finish_time",
              "time_lag", "odds", "prize"]
    model = Result
    readonly_fields = fields
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
    search_fields = ["key", "race__race_id", "race__title", "horse_name"]


class PmodelAdmin(admin.ModelAdmin):
    list_display = ("title", "method", "columns", "recall", "precision", "roi", "updated_at")


class LogAdmin(admin.ModelAdmin):
    ordering = ["-start_time", "pid"]
    list_display = ("start_time", "pid", "label", "exec_time", "finish")


admin.site.register(Race, RaceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Pmodel, PmodelAdmin)
admin.site.register(Log, LogAdmin)
