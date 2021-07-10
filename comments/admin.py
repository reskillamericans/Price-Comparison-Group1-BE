from django.contrib import admin

from .models import Comment  # Post


# Register your models here.

# admin.site.register(Post)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'body', 'created_on', 'edited')
    list_filter = ('active', 'product', 'created_on')
    search_fields = ('user', 'product', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
