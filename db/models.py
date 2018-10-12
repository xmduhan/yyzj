from django.db import models

# Create your models here.


class LfasrModel(models.Model):
    """ """
    md5 = models.CharField(max_length=256, primary_key=True)
    filename = models.CharField(max_length=1024, null=True, blank=True)
    task_id = models.CharField(max_length=256, null=True, blank=True)
    step = models.CharField(max_length=32, choices=(('upload', u'上传'), ('processing', u'处理中'), ('finish', u'完成')))
    code = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=1024, null=True, blank=True)
    data = models.TextField(null=True, blank=True)


class BatchModel(models.Model):
    """ """
    mail = models.CharField(max_length=1024)


class BatchItemModel(models.Model):
    """ """
    batch = models.ForeignKey(BatchModel, on_delete=models.CASCADE)
    lfasr = models.ForeignKey(LfasrModel, on_delete=models.SET_NULL, null=True, blank=True)
