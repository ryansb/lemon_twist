#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shlex import split
from twisted.python import log
from twisted.python.log import logging
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.threads import deferToThread
from lemon.util.errors import NotEnoughArgumentsException

required_args = dict(
    USER=1,
    PASS=1,
    IBUTTON=1,
    MACHINE=1,
    DROP=1,
    RAND=0,
    STAT=0,
    TEMP=0,
    GETBALANCE=0,
    ADDCREDITS=2,
    SENDCREDITS=2,
    EDITSLOT=6,
    ISVALIDUSER=1,
    QUERYADMIN=1,
    LOG=0,
    LOCATION=0,
    VERSION=0,
    CODE=2,
    UPTIME=0,
    QUIT=0,
)

machine_required = [
    "DROP",
    "RAND",
    "STAT",
    "TEMP",
    "EDITSLOT",
    "LOCATION",
]


def parseLine(line):
    line = split(line)
    cmd = line[0].upper()
    args = []
    if len(line) > 1:
        args = line[1:]
    if not len(args) >= required_args[cmd]:
        msg = ("Not enough arguments. Command %s requires %s arguments, "
               "%s given.")
        raise NotEnoughArgumentsException(msg % (
            cmd, required_args[cmd], len(args))
        )
    return cmd, args


class Lemon(LineReceiver):
    def __init__(self, users, config):
        self.config = config
        self.users = users
        self.name = None
        self.state = ""
        self.machine = None
        self.blank = False

    def connectionMade(self):
        #TODO: Log that a connection was started
        pass

    def connectionLost(self, reason):
        #TODO: Log connection closure
        if self.name in self.users:
            del self.users[self.name]
        print reason

    def lineReceived(self, line):
        if not len(line.strip()):
            if self.blank:
                self.loseConnection()
                return
            self.blank = True
        else:
            self.blank = False
        try:
            cmd, args = parseLine(line)
        except NotEnoughArgumentsException, e:
            log.msg(e.message, logLevel=logging.WARN)
            self.sendLine("ERR 406 Invalid Parameters.")
            return

        # how about we don't put passwords in the logs?
        if not cmd in ['IBUTTON', 'PASS']:
            log.msg("Received command:", line)
        else:
            log.msg("Received command:", cmd, "*****")

        if not hasattr(self, "handle_" + cmd):
            self.sendLine("ERR 452 Invalid command.")
            return
        if cmd in machine_required and self.machine is None:
            self.sendLine("ERR 407 Select machine.")
            return
        getattr(self, "handle_" + cmd)(*args)

    def handle_QUIT(self):
        self.loseConnection()

    def handle_USER(self, uname):
        #TODO: Check uname exists in LDAP
        self.users[uname] = self
        self.name = uname
        self.STATE = "SYN"
        if uname:
            self.sendLine("OK")

    def handle_WHOAMI(self):
        #TODO: check current user
        if self.STATE == "AUTH":
            #TODO: Get number of credits
            self.sendLine("OK: %s" % self.name)
        else:
            self.sendLine("ERR 204 You need to login.")

    def handle_PASS(self, *args):
        #TODO: check password against username
        password = args[0]
        if self.STATE is not "SYN":
            self.sendLine("ERR 201 USER command needs to be issued first.")
            return

        def callBack():
            self.state = "AUTH"
            numcredits = 0
            self.sendLine("OK Credits: %s" % numcredits)

        def errBack():
            self.sendLine("ERR 407 Invalid password.")

        #TODO: threadpool call to authenticate the user
        d = deferToThread(password)
        d.addCallback(callBack)
        d.addErrback(errBack)

    def handle_IBUTTON(self, *args):
        ibutton = args[0]
        #TODO: check ibutton against LDAP
        if ibutton:
            self.STATE = "AUTH"
            #TODO: Get number of credits
            numcredits = 0
            self.sendLine("OK: %s" % numcredits)
        else:
            self.STATE = "DENIED"
            self.sendLine("ERR 207 Invalid Ibutton.")

    def handle_MACHINE(self, machine):
        self.machine = machine
        if machine not in ['d', 'ld', 's']:
            self.sendLine("ERR 414 Invalid machine name - USAGE: "
                          "MACHINE < d | ld | s >")
        #TODO: grab information about machines
        machine_slots = []
        for slot in machine_slots:
            self.sendLine(repr(slot))

    def handle_STAT(self):
        #TODO: Get status of machine
        # getStatus(self.machine)
        try:
            machine_slots = []
            for slot in machine_slots:
                self.sendLine(repr(slot))
                # Slot repr format:
                # <slot num(int)> <slot name(string)> <slot price(int)> <num available(int)> <slot status(bool)>\n
            self.sendLine("OK %s Slots retrieved" % len(machine_slots))
        except:
            self.sendLine("ERR 416 Machine is offline or unreachable")

    def handle_GETBALANCE(self):
        if not self.state == "AUTH":
            self.sendLine("ERR 204 You need to login.")
        else:
            #TODO: get user balance from LDAP
            numcredits = 0
            self.sendLine("OK: %s" % numcredits)

    def handle_DROP(self, args):
        args = args.split(' ')
        slot = args[0]
        delay = (0 if len(args) == 1 else args[1])
        if not self.machine:
            # ERR 103 Unknown Failure.
            # ERR 150 Unable to initialize hardware for drop.
            self.sendLine("ERR 103 Unknown Failure.")
        #TODO: Drop a drink
        self.sendLine("Dropping drink")

    def handle_ADDCREDITS(self, *args):
        numcredits, dest = args.split(' ')
        try:
            #TODO: add the credits
            self.sendLine("OK: ")
        except:
            # ERR 208 Transfer error - user doesnt exist.
            # ERR 209 Error during credit transfer.
            self.sendLine("ERR 208")

    def handle_SENDCREDITS(self, *args):
        dest, numcredits = args.split(' ')
        try:
            #TODO: transfer the credits from issuing user to destination user
            self.sendLine("OK: ")
        except:
            # ERR 208 Transfer error - user doesnt exist.
            # ERR 209 Error during credit transfer.
            self.sendLine("ERR 208")

    def handle_UPTIME(self):
        #TODO: Get the server's uptime, we haven't actually been up since the
        # start of the epoch
        self.sendLine("OK: Up since: Thu, 1 Jan 1970 00:00:00 UTC")


class LemonFactory(Factory):
    config = None

    def __init__(self):
        self.users = {}  # maps user names to Lemon protocol instances

    def buildProtocol(self, addr):
        return Lemon(users=self.users, config=self.config)
