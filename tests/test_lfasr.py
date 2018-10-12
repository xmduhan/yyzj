#!/usr/bin/env python
# encoding: utf-8

import environment
from lfasr import add_lfasr_task
del environment


def test_add_lfasr_task():
    """ """
    lfasr = add_lfasr_task('wav/test.wav')
    print(lfasr.md5)
