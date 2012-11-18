#!/usr/bin/env python
# -*- coding: utf-8 -*-

# the sources of lemons, the trees
# machines, slots
import sqlalchemy as sa
from lemon.peel import Base
from sqlalchemy.orm import relationship


class Machine(Base):
    __tablename__ = 'machines'
    mid = sa.Column(sa.SmallInteger(unsigned=True),
                    primary_key=True,
                    nullable=False)
    machine_name = sa.Column(sa.String(length=255),
                             nullable=True)
    short_name = sa.Column(sa.String(length=7),
                           nullable=True)
    #slots a list of all the slots in the machine
    deleted = sa.Column(sa.Boolean,
                        default=False)
    public_ip = sa.Column(sa.String(length=15),
                          nullable=True)
    machine_ip = sa.Column(sa.String(length=15),
                           nullable=True)
    password = sa.Column(sa.String(length=255),
                         nullable=False)
    available_sensor = sa.Column(sa.Boolean,
                                 default=False,
                                 nullable=False)
    allow_connect = sa.Column(sa.Boolean,
                              default=True,
                              nullable=False)
    admin_only = sa.Column(sa.Boolean,
                           default=False,
                           nullable=False)
    location = sa.Column(sa.String(length=255),
                         nullable=True)

    def __repr__(self):
        if self.deleted:
            return ("<Deleted Machine %s (%s), mid: %s public_ip: %s "
                    "connections allowed: %s>" % (
                        self.machine_name, self.short_name, self.mid,
                        self.public_ip, self.allow_connect)
                    )
        return ("<Machine %s (%s), mid: %s public_ip: %s "
                "connections allowed: %s>" % (
                    self.machine_name, self.short_name, self.mid,
                    self.public_ip, self.allow_connect)
                )


class Slot(Base):
    __tablename__ = 'slots'
    id = sa.Column(sa.Integer,
                   primary_key=True,
                   nullable=False)
    mid = sa.Column(sa.SmallInteger(unsigned=True),
                    sa.ForeignKey('machines.mid'),
                    nullable=False)
    machine = relationship('Machine',
                           backref='slots',
                           order_by="Slot.slot_num")
    slot_num = sa.Column(sa.SmallInteger(unsigned=True),
                         nullable=False)
    slot_name = sa.Column(sa.String(length=255),
                          nullable=True)
    price = sa.Column(sa.Integer(unsigned=True),
                      nullable=True)
    availability = sa.Column(sa.SmallInteger(unsigned=True),
                             nullable=False,
                             default=0)

    def __repr__(self):
        return "<Slot #%s in %s, name: \"%s\" price: %s available: %s>" % (
            self.slot_num, self.machine.machine_name, self.slot_name,
            self.price, self.availability)
