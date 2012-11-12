#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Model(Base):
    pass

    ### Schema ###
    metadata = sa.MetaData()

    # Done
    drink_users = sa.Table(
        'drink_users',
        metadata,
        sa.Column('drink_id',
                  sa.Integer(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('user_name',
                  sa.String(length=255),
                  nullable=False),
        sa.Column('uid',
                  sa.Integer(unsigned=True),
                  nullable=True),
    )

    # Done
    status_id = sa.Table(
        'status_id',
        metadata,
        sa.Column('stat_id',
                  sa.Integer(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('stat_name',
                  sa.String(length=512),
                  nullable=False),
    )

    # Done
    machine_id = sa.Table(
        'machine_id',
        metadata,
        sa.Column('mid',
                  sa.SmallInteger(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('name',
                  sa.String(length=255),
                  nullable=True),
        sa.Column('deleted',
                  sa.Boolean,
                  default=False),
    )

    # Drop
    machine_ip = sa.Table(
        'machine_ip',
        metadata,
        sa.Column('mid',
                  sa.SmallInteger(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('public_ip',
                  sa.String(length=15),
                  nullable=True),
        sa.Column('machine_ip',
                  sa.String(length=15),
                  nullable=True),
    )

    # Drop
    machine_property = sa.Table(
        'machine_property',
        metadata,
        sa.Column('mid',
                  sa.SmallInteger(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('password',
                  sa.String(length=255),
                  nullable=False),
        sa.Column('available_sensor',
                  sa.Boolean,
                  default=False,
                  nullable=False),
        sa.Column('allow_connect',
                  sa.Boolean,
                  default=True,
                  nullable=False),
        sa.Column('admin_only',
                  sa.Boolean,
                  default=False,
                  nullable=False),
        sa.Column('location',
                  sa.String(length=255),
                  nullable=True),
    )

    # Done
    slot_property = sa.Table(
        'slot_property',
        metadata,
        sa.Column('mid',
                  sa.SmallInteger(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('slot_num',
                  sa.TinyInteger(unsigned=True),
                  nullable=False),
        sa.Column('slot_name',
                  sa.String(length=255),
                  nullable=True),
        sa.Column('price',
                  sa.Integer(unsigned=True),
                  nullable=True),
        sa.Column('availability',
                  sa.SmallInteger(unsigned=True),
                  nullable=False,
                  default=0),
        sa.Column('location',
                  sa.String(length=255),
                  nullable=True),
    )

    # Done
    temperature_log = sa.Table(
        'temperature_log',
        metadata,
        sa.Column('mid',
                  sa.SmallInteger(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('time',
                  sa.DateTime,
                  nullable=False),
        sa.Column('temp',
                  sa.Float,
                  nullable=True),
    )

    # Done
    drop_log = sa.Table(
        'drop_log',
        metadata,
        sa.Column('mid',
                  sa.SmallInteger(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('time',
                  sa.DateTime,
                  nullable=False),
        sa.Column('slot_name',
                  sa.String(length=255),
                  nullable=True),
        sa.Column('drink_id',
                  sa.Integer(unsigned=True),
                  sa.ForeignKey('drink_users.drink_id'),
                  nullable=False),
        sa.Column('stat_id',
                  sa.SmallInteger(unsigned=True),
                  nullable=False),
    )

    money_log = sa.Table(
        'money_log',
        metadata,
        sa.Column('mid',
                  sa.SmallInteger(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('time',
                  sa.DateTime,
                  nullable=False),
        sa.Column('drink_id',
                  sa.Integer(unsigned=True),
                  sa.ForeignKey('drink_users.drink_id'),
                  nullable=False),
        sa.Column('admin_id',
                  sa.Integer(unsigned=True),
                  sa.ForeignKey('drink_users.drink_id'),
                  nullable=False),
        sa.Column('amount',
                  sa.Integer(unsigned=True),
                  nullable=False),
        sa.Column('reason',
                  sa.String(length=255),
                  nullable=False),
    )

    app_id = sa.Table(
        'app_id',
        metadata,
        sa.Column('aid',
                  sa.SmallInteger(unsigned=True),
                  primary_key=True,
                  nullable=False),
        sa.Column('name',
                  sa.String(length=255),
                  nullable=True),
    )

    app_info = sa.Table(
        'app_info',
        metadata,
        sa.Column('aid',
                  sa.SmallInteger(unsigned=True),
                  sa.ForeignKey('app_id.aid'),
                  primary_key=True,
                  nullable=False),
        sa.Column('owner',
                  sa.Integer(unsigned=True),
                  sa.ForeignKey('drink_users.drink_id'),
                  primary_key=True,
                  nullable=False),
        sa.Column('description',
                  sa.String(length=255),
                  nullable=True),
    )

    app_prop = sa.Table(
        'app_prop',
        metadata,
        sa.Column('aid',
                  sa.SmallInteger(unsigned=True),
                  sa.ForeignKey('app_id.aid'),
                  primary_key=True,
                  nullable=False),
        sa.Column('public_key',
                  sa.String(length=4096),
                  nullable=True),
        sa.Column('owner_only',
                  sa.Boolean,
                  default=False,
                  nullable=False),
    )

    app_users = sa.Table(
        'app_users',
        metadata,
        sa.Column('aid',
                  sa.SmallInteger(unsigned=True),
                  sa.ForeignKey('app_id.aid'),
                  primary_key=True,
                  nullable=False),
        sa.Column('drink_id',
                  sa.Integer(unsigned=True),
                  sa.ForeignKey('drink_users.drink_id'),
                  primary_key=True,
                  nullable=False),
        sa.Column('date_granted',
                  sa.DateTime,
                  nullable=False),
    )

    app_used = sa.Table(
        'app_used',
        metadata,
        sa.Column('aid',
                  sa.SmallInteger(unsigned=True),
                  sa.ForeignKey('app_id.aid'),
                  primary_key=True,
                  nullable=False),
        sa.Column('drink_id',
                  sa.Integer(unsigned=True),
                  sa.ForeignKey('drink_users.drink_id'),
                  primary_key=True,
                  nullable=False),
        sa.Column('time',
                  sa.DateTime,
                  nullable=False),
    )
