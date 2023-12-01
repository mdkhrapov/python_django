from django.contrib.sitemaps import Sitemap

from .models import Article

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(selfs):
        return Article.objects.filter(published_at__isnull=False).order_by("-published_at")

    def lastmod(self, obj:Article):
        return obj.published_at

    def item_link(self, item: Article):
        return reverse("blogapp:article", kwargs={"pk": item.pk})