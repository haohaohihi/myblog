from django.contrib import admin
from blog.models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title', 'desc', 'click_count',)
    list_display_links = ('title', 'desc', 'click_count',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'username', 'pid',)
    fields = ('article', 'username', 'pid ')

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'index',)

class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'callback_url', 'index',)

class LinksAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'callback_url', 'index',)

admin.site.register(User)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(Column)
admin.site.register(Slogan)
