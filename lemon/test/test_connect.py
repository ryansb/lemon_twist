#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for L{lemon.twist.Lemon}
"""
from twisted.trial import unittest
from twisted.test import proto_helpers
from lemon.twist import LemonFactory


class TestNewConnection(unittest.TestCase):
    def setUp(self):
        factory = RemoteCalculationFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def _test(self, cmd, expected):
        self.proto.dataReceived('%s %d %d\r\n' % (operation, a, b))
        self.assertEqual(int(self.tr.value()), expected)

    def test_new_connections(self):
        return self._test("")
