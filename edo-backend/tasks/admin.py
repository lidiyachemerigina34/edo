from django.contrib import admin

from tasks.models import TaskModel, TaskCommentsModel


class TasksAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(TaskModel,TasksAdmin)
admin.site.register(TaskCommentsModel,TasksAdmin)