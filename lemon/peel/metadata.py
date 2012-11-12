#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Information about peels. Status info table.
# status_id
import sqlalchemy as sa
from lemon.peel import Model


class StatusId(Base):
    __tablename__ = 'status_id'
    stat_id   = sa.Column(sa.Integer(unsigned=True),
                          primary_key=True,
                          nullable=False)
    stat_name = sa.Column(sa.String(length=512),
                          nullable=False)
