#!/usr/bin/env python
# -*- coding: utf-8 -*-

# the sources of lemons, the trees
# machines, slots
import sqlalchemy as sa
from lemon.peel import Model


class Machine(Model):
    __tablename__ = 'machines',
    mid              = sa.Column(sa.SmallInteger(unsigned=True),
                                 primary_key=True,
                                 nullable=False)
    name             = sa.Column(sa.String(length=255),
                                 nullable=True)
    deleted          = sa.Column(sa.Boolean,
                                 default=False)
    public_ip        = sa.Column(sa.String(length=15),
                                 nullable=True)
    machine_ip       = sa.Column(sa.String(length=15),
                                 nullable=True)
    password         = sa.Column(sa.String(length=255),
                                 nullable=False)
    available_sensor = sa.Column(sa.Boolean,
                                 default=False,
                                 nullable=False)
    allow_connect    = sa.Column(sa.Boolean,
                                 default=True,
                                 nullable=False)
    admin_only       = sa.Column(sa.Boolean,
                                 default=False,
                                 nullable=False)
    location         = sa.Column(sa.String(length=255),
                                 nullable=True)


class Slot(Model):
    __tablename__ = 'slots',
    mid          = sa.Column(sa.SmallInteger(unsigned=True),
                             sa.ForeignKey('machines.mid'),
                             nullable=False)
    machine      = sa.relationship("Machine",
                                   backref=sa.backref(
                                       'machines',
                                       lazy='dynamic')
                                   )
    slot_num     = sa.Column(sa.TinyInteger(unsigned=True),
                             nullable=False)
    slot_name    = sa.Column(sa.String(length=255),
                             nullable=True)
    price        = sa.Column(sa.Integer(unsigned=True),
                             nullable=True)
    availability = sa.Column(sa.SmallInteger(unsigned=True),
                             nullable=False,
                             default=0)
