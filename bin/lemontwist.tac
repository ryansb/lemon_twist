from copy import deepcopy
from lemon.util.conf import LemonConfig
from lemon.twist import LemonFactory
from twisted.python import log, util
from twisted.application import service
from twisted.python.logfile import LogFile
from twisted.application.internet import TCPServer


class FormattedLogObserver(log.FileLogObserver):
    """Custom Logging observer"""
    def emit(self, eventDict):
        """Custom emit for FileLogObserver"""
        text = log.textFromEventDict(eventDict)
        if text is None:
            return
        self.timeFormat = '[%Y-%m-%d %H:%M:%S]'
        timeStr = self.formatTime(eventDict['time'])
        fmtDict = {'text': text.replace("\n", "\n\t")}
        msgStr = log._safeFormat("%(text)s\n", fmtDict)
        util.untilConcludes(self.write, timeStr + " LemonTwist " + msgStr)
        util.untilConcludes(self.flush)


class LemonTwistService(service.Service):
    def __init__(self, config):
        self.config = config

    def getLemonTwistFactory(self):
        factory = LemonFactory()
        factory.config = deepcopy(self.config)
        return LemonFactory()

application = service.Application('lemontwist', uid=1000, gid=1000)

s = LemonTwistService(LemonConfig.loadConfig("conf/lemon.cfg"))

serviceCollection = service.IServiceCollection(application)
TCPServer(s.config.port, s.getLemonTwistFactory()
          ).setServiceParent(serviceCollection)

# Log to /tmp for now
logfile = LogFile("lemontwist.log", "/tmp", rotateLength=None)
application.setComponent(log.ILogObserver, FormattedLogObserver(logfile).emit)
