#!/usr/bin/env python
# encoding: utf-8
import environment
import hashlib
from db.models import LfasrModel
del environment


def add_lfasr_task(filename):
    """ """
    md5 = hashlib.md5(open(filename, 'rb').read()).hexdigest()
    lfasr, created = LfasrModel.objects.get_or_create(md5=md5)
    if created:
        lfasr.__dict__.update(filename=filename, step='upload')
        lfasr.save()
    return lfasr
