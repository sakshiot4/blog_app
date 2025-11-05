import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

# Define a feed for the latest blog posts.
class LatestPostsFeed(Feed): #this class inherits from Feed class.
    title = "My blog"
    link = reverse_lazy("blog:post_list") #link to the blog's post list page.
    description = "New Posts of my Blog."

    def items(self):
        return Post.published.all()[:5] #return the latest 5 published posts.
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30) #convert the body from markdown to HTML and truncate it to 30 words.    
    
    def item_pupdate(self, item):
        return item.publish #return the publish date of the post.