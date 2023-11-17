from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Article, Tag

class ArticleInline(admin.TabularInline):
    model = Tag.tag.through


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ArticleInline,
    ]
    list_display = "title", "content", "pub_date", "author", "category"

    def get_queryset(self, request):
        return Article.objects.select_related("category").prefetch_related("tags").all()


