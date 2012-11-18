#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lemon.peel.users import User
from lemon.util.ldap import userCheck
from lemon.util.errors import UserNonExistentException, BadCredentialsException


def authUser(proto, password):
    try:
        user = User.query('user_name' == proto.uname).all()[0]
    except IndexError:
        raise UserNonExistentException("User %s does not exist" % proto.uname)
    if userCheck(user.user_name, password):
        return True
    raise BadCredentialsException("Invalid password for user %s" % user.user_name)
