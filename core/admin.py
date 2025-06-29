from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'completed')
    search_fields = ('title', 'description')
    list_filter = ('completed', 'created_at')
    ordering = ('-created_at',)