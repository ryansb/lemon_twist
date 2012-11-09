from lemon.twist import Lemon
from copy import deepcopy
from lemon.conf import LemonConfig
from lemon.twist import LemonFactory
from twisted.application import service
from twisted.python.logfile import LogFile
from twisted.application.internet import TCPServer
from twisted.internet import protocol
from twisted.python.log import ILogObserver, FileLogObserver


class LemonTwistService(service.Service):
    def getLemonTwistFactory(self):
        factory = LemonFactory()
        factory.config = deepcopy(self.config)
        return LemonFactory()

application = service.Application('lemontwist', uid=1000, gid=1000)

s = LemonTwistService()
s.config = LemonConfig.loadConfig("conf/lemon.cfg")

serviceCollection = service.IServiceCollection(application)
print type(s.config.port)
TCPServer(s.config.port, s.getLemonTwistFactory()
          ).setServiceParent(serviceCollection)

# Log to /tmp for now
logfile = LogFile("lemontwist.log", "/tmp", rotateLength=None)
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
