#!/usr/bin/env python
# encoding: utf-8

import py4j
from py4j.java_gateway import JavaGateway, GatewayParameters
import json

port = py4j.java_gateway.launch_gateway(classpath='jvm/libs/*:jvm')
gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))

def test():
    """ """
    LfasrClientImp = gateway.jvm.com.iflytek.msp.cpdb.lfasr.client.LfasrClientImp
    lc = LfasrClientImp.initLfasrClient()
    LfasrType = gateway.jvm.com.iflytek.msp.cpdb.lfasr.model.LfasrType

    params = gateway.jvm.java.util.HashMap()
    params['has_participle'] = 'true'

    # upload_result = lc.lfasrUpload('test.wav', LfasrType.LFASR_STANDARD_RECORDED_AUDIO, params)
    upload_result = lc.lfasrUpload('test.wav', LfasrType.LFASR_TELEPHONY_RECORDED_AUDIO, params)
    upload_result.getOk()
    task_id = upload_result.getData()
    task_id

