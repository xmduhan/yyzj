from django.contrib import admin
from . import models

# Register your models here.


class LfasrAdmin(admin.ModelAdmin):
    """ """


admin.site.register(models.LfasrModel, LfasrAdmin)


class MailAdmin(admin.ModelAdmin):
    """ """


admin.site.register(models.MailModel, models.MailAdmin)
