from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly" #how frequently the content is likely to change.
    priority = 0.9 #priority of this URL relative to other URLs on your site.

    def items(self):
        return Post.published.all() #returns all published posts.   
    
    def lastmod(self, obj):
        return obj.updated #returns the last modified time of the post.
        