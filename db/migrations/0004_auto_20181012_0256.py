# Generated by Django 2.1.2 on 2018-10-12 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_auto_20181012_0148'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchItemModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BatchModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.CharField(max_length=1024)),
            ],
        ),
        migrations.RenameField(
            model_name='lfasrmodel',
            old_name='path',
            new_name='filename',
        ),
        migrations.AddField(
            model_name='lfasrmodel',
            name='task_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='batchitemmodel',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.BatchModel'),
        ),
        migrations.AddField(
            model_name='batchitemmodel',
            name='lfasr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.LfasrModel'),
        ),
    ]