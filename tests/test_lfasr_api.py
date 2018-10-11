#!/usr/bin/env python
# encoding: utf-8

import json
from time import sleep

from gateway import JavaGateway


def test_lfasr_api():
    """ """
    # Load JVM
    gateway = JavaGateway()
    LfasrType = gateway.jvm.com.iflytek.msp.cpdb.lfasr.model.LfasrType
    LfasrClientImp = gateway.jvm.com.iflytek.msp.cpdb.lfasr.client.LfasrClientImp
    lc = LfasrClientImp.initLfasrClient()

    # Upload wav file
    params = gateway.jvm.java.util.HashMap()
    params['has_participle'] = 'true'
    # Upload = lc.lfasrUpload('test.wav', LfasrType.LFASR_STANDARD_RECORDED_AUDIO, params)
    upload = lc.lfasrUpload('wav/test.wav', LfasrType.LFASR_TELEPHONY_RECORDED_AUDIO, params)
    assert upload.getOk() == 0
    task_id = upload.getData()

    # Wait server
    while True:
        progress = lc.lfasrGetProgress(task_id)
        assert progress.getOk() == 0
        data = json.loads(progress.getData())
        print(data)
        if data['status'] == 9:
            break
        sleep(3)

    # Read result
    result = lc.lfasrGetResult(task_id)
    assert result.getOk() == 0
    data = json.loads(result.getData())
    print(','.join([segment['onebest'] for segment in data]))
