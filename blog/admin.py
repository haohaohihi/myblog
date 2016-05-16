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
    fieldsets = (
        (
            None, {
                'fields': ('title', 'desc', 'content')
            },
        ),
        ('高级设置', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend')
        })
    )

##################################有问题################
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'username', 'pid',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'index',)

class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'callback_url', 'index',)

class LinksAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'callback_url', 'index',)

admin.site.register(User)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Links, LinksAdmin)
