from django.contrib import admin
from . import models

# Register your models here.


class LfasrAdmin(admin.ModelAdmin):
    """ """
    list_display = ['md5', 'filename', 'task_id', 'step', 'code', 'message', 'data']


admin.site.register(models.LfasrModel, LfasrAdmin)


class MailAdmin(admin.ModelAdmin):
    """ """
    list_display = ['subject', 'date', 'mailfrom', 'message_id']


admin.site.register(models.MailModel, MailAdmin)
