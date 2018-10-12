#!/usr/bin/env python
# encoding: utf-8

import environment
import lfasr
del environment


def test_add_task():
    """ """
    lfasr_model = lfasr.add_task('wav/test.wav')
    print(lfasr_model.md5)
