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


class BatchAdmin(admin.ModelAdmin):
    """ """
    list_display = ['mail']


admin.site.register(models.BatchModel, BatchAdmin)


class BatchItemAdmin(admin.ModelAdmin):
    """ """
    list_display = ['batch', 'lfasr']


admin.site.register(models.BatchItemModel, BatchItemAdmin)
