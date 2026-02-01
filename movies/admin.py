from django.contrib import admin
from .models import Movie, Review, ReviewReport

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(ReviewReport)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "user", "is_active", "date")
    list_filter = ("is_active", "date")
    search_fields = ("comment", "user__username", "movie__name")
    def report_count(self, obj):
        return obj.reports.count()


class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ("id", "movie_name", "review_comment", "review_author", "reporter", "created_at")
    list_select_related = ("review", "review__movie", "review__user", "reporter")
    search_fields = ("review__comment", "review__movie__name", "review__user__username", "reporter__username")
    readonly_fields = ("created_at",)

    def movie_name(self, obj):
        return obj.review.movie.name

    def review_author(self, obj):
        return obj.review.user.username

    def review_comment(self, obj):
        # show a short preview so admin list isn't huge
        text = obj.review.comment
        return text if len(text) <= 60 else text[:60] + "..."