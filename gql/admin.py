from django.contrib import admin

from .models import Publish, Category, Comment


@admin.register(Publish)
class PublishAdmin(admin.ModelAdmin):
    autocomplete_fields = ['categories']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
