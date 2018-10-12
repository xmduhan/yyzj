#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import django

path = os.getcwd()
settings = '%s.settings' % path.split('/')[-1]
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

django.setup()
