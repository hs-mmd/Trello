from django.contrib import admin
from .models import Workspace, Task, Board, Tag

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created']
    list_filter = ['owner', 'created']
    search_fields = ['name', 'owner__username']
    filter_horizontal = ['members']
    ordering = ['-created']
    readonly_fields = ['created']

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    filter_horizontal = ('tags',)
    show_change_link = True
    fields = ('title', 'status', 'assignee', 'start_date', 'due_date')



@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'workspace', 'created', 'tasks_count')
    search_fields = ('title',)
    list_filter = ('workspace',)
    inlines = [TaskInline]

    def tasks_count(self, obj):
        return obj.tasks.count()
    tasks_count.short_description = 'Number of Tasks'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'status', 'assignee', 'due_date', 'created')
    list_filter = ('status', 'board', 'assignee', 'tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)