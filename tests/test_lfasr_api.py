#!/usr/bin/env python
# encoding: utf-8

import lfasr
from time import sleep


def test_lfasr_api():
    """ """
    # Upload wav file
    code, message, task_id = lfasr.upload('wav/test.wav')
    assert code == 0

    # Wait for server processing
    while True:
        code, message, data = lfasr.query_progress(task_id)
        assert code == 0
        print(data)
        if data['status'] == 9:
            break
        sleep(3)

    # Read result
    code, message, data = lfasr.get_result(task_id)
    assert code == 0
    print(','.join([segment['onebest'] for segment in data]))
