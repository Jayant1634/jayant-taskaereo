from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'updated_date')
    search_fields = ('title', 'description')
    ordering = ('-created_date',)
