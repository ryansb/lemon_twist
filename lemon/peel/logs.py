#!/usr/bin/env python
# -*- coding: utf-8 -*-

# logging and history peels
# drop_log, temperature_log, money_log
import sqlalchemy as sa
from datetime import datetime
from lemon.peel import Base
from lemon.peel.users import User
from lemon.peel.metadata import StatusId
from sqlalchemy.orm import relationship, deferred


class DropLog(Base):
    __tablename__ = 'drop_log'
    id = sa.Column(sa.Integer,
                   primary_key=True,
                   nullable=False)
    mid = sa.Column(sa.SmallInteger(unsigned=True),
                    nullable=False)
    time = sa.Column(sa.DateTime,
                     nullable=False)
    slot_name = sa.Column(sa.String(length=255),
                          nullable=True)
    drink_id = sa.Column(sa.Integer(unsigned=True),
                         sa.ForeignKey('drink_users.drink_id'),
                         nullable=False)
    drink_user = relationship('User', backref='drop_logs')
    stat_id = sa.Column(sa.SmallInteger(unsigned=True),
                        sa.ForeignKey('status_id.stat_id'),
                        nullable=False)
    stat = relationship('StatusId')

    def __repr__(self):
        return ("DropLog: <%s> mid: <%s> slot_name: \"%s\" "
                "user: <%s> status: \"%s\"" % (
                self.time, self.mid, self.slot_name, self.drink_user.user_name,
                self.stat.stat_name))


class TemperatureLog(Base):
    __tablename__ = 'temperature_log'
    id = sa.Column(sa.Integer,
                   primary_key=True,
                   nullable=False)
    mid = sa.Column(sa.SmallInteger(unsigned=True),
                    nullable=False)
    time = sa.Column(sa.DateTime,
                     nullable=False)
    temp = sa.Column(sa.Float,
                     nullable=True)

    def __repr__(self):
        return "TemperatureLog: <%s> mid: \"%s\" temp: <%s>" % (
            self.time, self.mid, self.temp)


class MoneyLog(Base):
    __tablename__ = 'money_log'
    id = sa.Column(sa.Integer,
                   primary_key=True,
                   nullable=False)
    mid = sa.Column(sa.SmallInteger(unsigned=True),
                    nullable=False)
    time = sa.Column(sa.DateTime,
                     default=datetime.now(),
                     nullable=False)
    drink_id = sa.Column(sa.Integer(unsigned=True),
                         sa.ForeignKey('drink_users.drink_id'),
                         nullable=False)
    drink_user = relationship("User", backref='money_logs',
                              primaryjoin="User.drink_id==MoneyLog.drink_id")
    admin_id = sa.Column(sa.Integer(unsigned=True),
                         sa.ForeignKey('drink_users.drink_id'),
                         nullable=False)
    admin_user = relationship("User", backref='admin_logs',
                              primaryjoin="User.drink_id==MoneyLog.admin_id")
    amount = sa.Column(sa.Integer(unsigned=True),
                       nullable=False)
    reason = sa.Column(sa.String(length=255),
                       nullable=False)

    def __repr__(self):
        return "MoneyLog: <%s> amount: <%s> user: <%s> admin: <%s> reason: \"%s\"" % (
            self.time, self.amount, self.drink_user.user_name, self.admin_user.user_name,
            self.reason)
