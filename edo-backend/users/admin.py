from django.contrib import admin

# Register your models here.
from users.models import UsersModel, DepartamentsModel, DepartamentUsersModel, RolesModel


class UsersAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(UsersModel,UsersAdmin)
admin.site.register(DepartamentsModel,UsersAdmin)
admin.site.register(DepartamentUsersModel,UsersAdmin)
admin.site.register(RolesModel,UsersAdmin)