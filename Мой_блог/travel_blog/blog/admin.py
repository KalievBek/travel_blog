from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_per_page = 20


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'country', 'created_at', 'updated_at')
    list_filter = ('category', 'country', 'created_at')
    search_fields = ('title', 'content', 'author')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'image'),
        }),
        ('Метаданные поста', {
            'fields': ('category', 'author', 'country'),
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    date_hierarchy = 'created_at'
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'created_at', 'post')
    search_fields = ('author', 'text')
    readonly_fields = ('created_at',)
    fields = ('post', 'author', 'text', 'is_published', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 20