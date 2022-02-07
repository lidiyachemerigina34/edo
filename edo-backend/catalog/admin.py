from django.contrib import admin

from catalog.models import FileModel,TemplateModel, ReconciliationModel, ReconciliationUsersModel, ReconciliationCommentsModel, ReconciliationFileModel


class FileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

admin.site.register(ReconciliationFileModel,FileAdmin)
admin.site.register(FileModel,FileAdmin)
admin.site.register(ReconciliationModel,FileAdmin)
admin.site.register(TemplateModel,FileAdmin)
admin.site.register(ReconciliationUsersModel,FileAdmin)
admin.site.register(ReconciliationCommentsModel,FileAdmin)