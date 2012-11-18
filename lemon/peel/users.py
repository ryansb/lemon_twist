#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Information about users. Maps CSH uid to a unique universal drink ID
# drink_users
import sqlalchemy as sa
from lemon.peel import Base


class User(Base):
    __tablename__ = 'drink_users'
    drink_id = sa.Column(sa.Integer(unsigned=True),
                         primary_key=True,
                         nullable=False)
    user_name = sa.Column(sa.String(length=255),
                          nullable=False)
    uid = sa.Column(sa.Integer(unsigned=True),
                    nullable=True)
    admin = sa.Column(sa.Boolean,
                      default=False,
                      nullable=False)
    #drop_logs, a list of all drops a user has made ordered by time
    #money_logs, a list of all transactions a user has made ordered by time
    #admin_logs, a list of all transactions in which a user has been an admin

    def __repr__(self):
        if self.admin:
            return "<Admin User: \"%s\" drink_id: %s uid: %s>" % (
                self.user_name, self.drink_id, self.uid)
        return "<User: \"%s\" drink_id: %s uid: %s>" % (
            self.user_name, self.drink_id, self.uid)
