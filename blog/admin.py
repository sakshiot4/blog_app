from django.contrib import admin

from .models import Post, Comment

# Register your models here.

#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"] #filter by these fields
    search_fields = ["title", "body"] #search by these fields.
    prepopulated_fields = {'slug': ("title", )} #auto fill slug field based on title
    raw_id_fields = ["author"] #use raw id field for author. Lookup by id.
    date_hierarchy = "publish" #add date hierarchy based on publish date.
    ordering = ["status", "publish"] #default ordering by status and publish date.
    show_facets = admin.ShowFacets.ALWAYS #always show facets in the admin interface.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"] #