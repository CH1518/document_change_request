from django.contrib import admin
from .import models
from .models import Comment, Request
# Register your models here.

# class GroupMemberInline(admin.TabularInline):
#     model = models.GroupMember

# admin.site.register(models.Group)
#admin.site.register(models.Area)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(Request)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_title', 'created_at', 'area','status')
    list_filter = ('user', 'document_title', 'created_at', 'area','status')
    search_fields = ('user', 'document_title', 'created_at', 'area','status')
