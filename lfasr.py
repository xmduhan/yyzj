#!/usr/bin/env python
# encoding: utf-8
import json
import environment
import hashlib
from db.models import LfasrModel
from gateway import JavaGateway
from time import sleep
del environment

gateway = JavaGateway()
LfasrType = gateway.jvm.com.iflytek.msp.cpdb.lfasr.model.LfasrType
LfasrClientImp = gateway.jvm.com.iflytek.msp.cpdb.lfasr.client.LfasrClientImp
lc = LfasrClientImp.initLfasrClient()


def add_task(filename):
    """ """
    md5 = hashlib.md5(open(filename, 'rb').read()).hexdigest()
    lfasr_model, created = LfasrModel.objects.get_or_create(md5=md5)
    if created:
        lfasr_model.__dict__.update(filename=filename, step='upload')
        code, message, task_id = upload(lfasr_model.filename)
        lfasr_model.__dict__.update(code=code, message=message, task_id=task_id)
        if code == 0:
            lfasr_model.step = 'processing'
        lfasr_model.save()
    return lfasr_model


def read_api_exception(e):
    """ """
    e = json.loads(e.java_exception.getMessage())
    return [e[k] for k in ('err_no', 'failed', 'data')]


def upload(filename, lfasr_type=LfasrType.LFASR_TELEPHONY_RECORDED_AUDIO):
    """
    filename  wav file to upload
    lfasr_type  can be LFASR_TELEPHONY_RECORDED_AUDIO or LFASR_STANDARD_RECORDED_AUDIO
    """
    try:
        params = gateway.jvm.java.util.HashMap()
        params['has_participle'] = 'true'
        upload = lc.lfasrUpload(filename, lfasr_type, params)
    except Exception as e:
        return read_api_exception(e)
    return upload.getErr_no(), upload.getFailed(), upload.getData()


def query_progress(task_id):
    """ """
    try:
        progress = lc.lfasrGetProgress(task_id)
    except Exception as e:
        return read_api_exception(e)
    # data = json.loads(progress.getData()) if progress.getOk() == 0 else None
    return progress.getErr_no(), progress.getFailed(), progress.getData()


def get_result(task_id):
    """ """
    try:
        result = lc.lfasrGetResult(task_id)
    except Exception as e:
        return read_api_exception(e)
    # data = json.loads(result.getData()) if result.getOk() == 0 else None
    return result.getErr_no(), result.getFailed(), result.getData()


def main():
    """ """
    while True:

        # # Upload wav file
        # for lfasr_model in LfasrModel.objects.filter(step='upload', code__isnull=True):
        #     print(u'Upload file: filename=%s ... ' % lfasr_model.filename, end='')
        #     code, message, task_id = upload(lfasr_model.filename)
        #     lfasr_model.__dict__.update(code=code, message=message, task_id=task_id)
        #     if code == 0:
        #         lfasr_model.step = 'processing'
        #     lfasr_model.save()
        #     sleep(1)
        #     print(u'(ok)')

        # Query progress
        for lfasr_model in LfasrModel.objects.filter(step='processing'):
            print(u'Query: task_id=%s ... ' % lfasr_model.task_id, end='')
            code, message, data = query_progress(lfasr_model.task_id)
            lfasr_model.__dict__.update(code=code, message=message, data=data)
            if code == 0:
                data = json.loads(data)
                if data['status'] == 9:
                    code, message, data = get_result(lfasr_model.task_id)
                    lfasr_model.__dict__.update(code=code, message=message, data=data, step='finish')
                    print('(finish) ...', end='')
            lfasr_model.save()
            sleep(1)
            print(u'(ok)')

        sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        gateway = None
        print()
