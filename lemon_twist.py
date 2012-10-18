#!/usr/bin/env python
# -*- coding; utf-8 -*-
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

class Lemon(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = ""
        self.machine = ""

    def connectionMade(self):
        #TODO: Log that a connection was started

    def connectionLost(self, reason):
        #TODO: Log connection closure
        if self.users.has_key(self.name):
            del self.users[self.name]

    def lineReceived(self, line):
        if not self.state:
            arg = ' '.join(line.split(' ')[1:].strip())
            if line.startswith("USER"):
                self.handle_USER(line)
            if line.startswith("IBUTTON"):
                self.handle_IBUTTON(line)
        else:
            self.handle_COMMAND(line)

    #def handle_CHAT(self, message):
    #    message = "<%s> %s" % (self.name, message)
    #    for name, protocol in self.users.iteritems():
    #        if protocol != self:
    #            protocol.sendLine(message)

    def handle_USER(self, uname):
        #TODO: Check uname exists in LDAP
        self.users[uname] = self
        self.name = uname
        self.STATE = "SYN"
        if uname:
            self.sendLine("OK")

    def handle_PASS(self, password):
        #TODO: check password against username
        if password:
            self.STATE = "AUTH"
            #TODO: Get number of credits
            numcredits = 0
            self.sendLine("OK: %s" % numcredits)
        else:
            self.STATE = "DENIED"
            self.sendLine("ERR 407 Invalid password.")
            self.loseConnection()

    def handle_IBUTTON(self, ibutton):
        #TODO: check ibutton against LDAP
        if ibutton:
            self.STATE = "AUTH"
            #TODO: Get number of credits
            numcredits = 0
            self.sendLine("OK: %s" % numcredits)
        else:
            self.STATE = "DENIED"
            self.sendLine("ERR 207 Invalid Ibutton.")
            self.loseConnection()

    def handle_MACHINE(self, machine):
        self.machine = machine
        if machine not in ['d', 'ld', 's']:
            self.sendLine("ERR 414 Invalid machine name - USAGE: MACHINE < d | ld | s >")
            self.loseConnection()
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
            self.loseConnection()
        #TODO: Drop a drink
        self.sendLine("Dropping drink")

    def handle_SENDCREDITS(self, args):
        numcredits, dest = args.split(' ')
        try:
            #TODO: transfer the credits
            self.sendLine("OK: ")
        except:
            # ERR 208 Transfer error - user doesnt exist.
            # ERR 209 Error during credit transfer.
            self.sendLine("ERR 208")

    def handle_UPTIME(self):
        #TODO: Get the server's uptime
        self.sendLine("OK: Up since: Wed, 16 Sept 1959 00:07:37 EST")


class LemonFactory(Factory):
    def __init__(self):
        self.users = {} # maps user names to Lemon protocol instances

    def buildProtocol(self, addr):
        return Lemon(self.users)


if __name__ == '__main__':
    reactor.listenTCP(8000, LemonFactory())
    reactor.run()