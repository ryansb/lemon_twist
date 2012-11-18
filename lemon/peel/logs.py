#!/usr/bin/env python
# -*- coding: utf-8 -*-

# logging and history peels
# drop_log, temperature_log, money_log
import sqlalchemy as sa
from lemon.peel import Base
from sqlalchemy.orm import relationship


class DropLog(Base):
    __tablename__ = 'drop_log'
    mid = sa.Column(sa.SmallInteger(unsigned=True),
                    primary_key=True,
                    nullable=False)
    time = sa.Column(sa.DateTime,
                     nullable=False)
    slot_name = sa.Column(sa.String(length=255),
                          nullable=True)
    drink_id = sa.Column(sa.Integer(unsigned=True),
                         sa.ForeignKey('drink_users.drink_id'),
                         nullable=False)
    user = relationship('User', backref='drop_logs')
    stat_id = sa.Column(sa.SmallInteger(unsigned=True),
                        sa.ForeignKey('status_id.stat_id'),
                        nullable=False)
    stat = relationship('StatusId')


class TemperatureLog(Base):
    __tablename__ = 'temperature_log'
    mid = sa.Column(sa.SmallInteger(unsigned=True),
                    primary_key=True,
                    nullable=False)
    time = sa.Column(sa.DateTime,
                     nullable=False)
    temp = sa.Column(sa.Float,
                     nullable=True)


class MoneyLog(Base):
    __tablename__ = 'money_log'
    mid = sa.Column(sa.SmallInteger(unsigned=True),
                    primary_key=True,
                    nullable=False)
    time = sa.Column(sa.DateTime,
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
