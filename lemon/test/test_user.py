#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for L{lemon.twist.Lemon}
"""
from twisted.trial import unittest
from lemon.peel import Base
from lemon.peel.users import User
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


class TestNewConnection(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite://')
        metadata = Base.metadata
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def test_new_user(self):
        u = User()
        u.user_name = 'ryansb'
        u.uid = 7
        u.admin = True
        self.session.add(u)
        self.session.commit()

        self.assertEqual(len(self.session.query(User).filter(
            User.user_name == 'ryansb').all()), 1)
        return False
