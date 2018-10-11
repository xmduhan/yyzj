#!/usr/bin/env python
# encoding: utf-8
import os
import py4j
from py4j.java_gateway import GatewayParameters, launch_gateway


class JavaGateway(py4j.java_gateway.JavaGateway):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        # path = os.path.realpath(__file__)
        path = os.path.dirname(os.path.realpath(__file__))
        print(path)
        print('{path}/libs/*:{path}'.format(**locals()))
        port = launch_gateway(classpath='{path}/libs/*:{path}'.format(**locals()))
        super(JavaGateway, self).__init__(gateway_parameters=GatewayParameters(port=port))

    def __del__(self):
        """ """
        self.shutdown()
