from django.contrib import admin
from testapp.models import Blog, Comments
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug','author', 'body', 'publish', 'created', 'update', 'atatus']
    list_filter = ('author', 'created', 'publish')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    # date_hierarchy = 'publish',
    ordering = ['atatus', 'publish']
    prepopulated_fields = {'slug':('title',)}


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'body', 'created', 'update', 'active']
    list_filter = ('active','update', 'created')
    search_fields = ('name', 'email', 'body')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comments, CommentsAdmin)
