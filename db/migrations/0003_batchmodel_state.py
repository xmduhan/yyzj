# Generated by Django 2.1.2 on 2018-10-17 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_batchitemmodel_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchmodel',
            name='state',
            field=models.CharField(blank=True, choices=[('processing', '处理中'), ('finish', '完成')], max_length=128, null=True),
        ),
    ]