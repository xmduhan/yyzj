#!/usr/bin/env python
# encoding: utf-8
import json
import environment
import hashlib
from db.models import LfasrModel
from gateway import JavaGateway
del environment

gateway = JavaGateway()
LfasrType = gateway.jvm.com.iflytek.msp.cpdb.lfasr.model.LfasrType
LfasrClientImp = gateway.jvm.com.iflytek.msp.cpdb.lfasr.client.LfasrClientImp
lc = LfasrClientImp.initLfasrClient()


def add_task(filename):
    """ """
    md5 = hashlib.md5(open(filename, 'rb').read()).hexdigest()
    lfasr, created = LfasrModel.objects.get_or_create(md5=md5)
    if created:
        lfasr.__dict__.update(filename=filename, step='upload')
        lfasr.save()
    return lfasr


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
    data = json.loads(progress.getData()) if progress.getOk() == 0 else None
    return progress.getErr_no(), progress.getFailed(), data


def get_result(task_id):
    """ """
    try:
        result = lc.lfasrGetResult(task_id)
    except Exception as e:
        return read_api_exception(e)
    data = json.loads(result.getData()) if result.getOk() == 0 else None
    return result.getErr_no(), result.getFailed(), data


def main():
    """ """
    for lfasr in LfasrModel.objects.filter(step='upload'):
        print(lfasr)


if __name__ == "__main__":
    main()
