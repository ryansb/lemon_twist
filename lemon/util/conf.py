import os
from twisted.python import log

from ConfigParser import ConfigParser


class ConfigErrors(Exception):

    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors[:]

    def __str__(self):
        return "\n".join(self.errors)

    def addError(self, msg):
        self.errors.append(msg)

    def __nonzero__(self):
        return len(self.errors)


_errors = None


def error(error):
    if _errors is not None:
        _errors.addError(error)
    else:
        raise ConfigErrors([error])


class LemonConfig(object):

    def __init__(self):
        # default values for all attributes
        self.title = 'lemon'

        self.db_url = None
        self.db_name = None
        self.db_user = None
        self.db_pass = None
        self.port = 9001

    @classmethod
    def loadConfig(cls, filename):
        if not os.path.exists(filename):
            raise ConfigErrors([
                "configuration file '%s' does not exist"
                % (filename,), ])

        cfg = ConfigParser()
        try:
            cfg.read(filename)
            log.msg("Loaded configuration from %s" % filename)
        except IOError, e:
            raise ConfigErrors([
                "unable to open configuration file %r: %s" % (
                filename, e), ])

        # from here on out we can batch errors together for convenience
        global _errors
        _errors = errors = ConfigErrors()

        # instantiate a new config object, which will apply defaults
        # automatically
        config = cls()

        # use configparser to load values
        config.db_url = cfg.get('DB', 'url', config.db_url)
        config.db_name = cfg.get('DB', 'name', config.db_name)
        config.db_user = cfg.get('DB', 'user', config.db_user)
        config.db_pass = cfg.get('DB', 'pass', config.db_pass)
        config.port = cfg.getint('Network', 'port')

        # run some sanity checks
        config.check_db(errors)

        if errors:
            raise errors

        return config

    def check_db(self, errors):
        # Make sure they provided database info
        if not self.db_url:
            errors.addError("No database url provided for database")
        if not self.db_name:
            errors.addError("No database name provided for database")
        if not self.db_user:
            errors.addError("No username provided for database")
        if not self.db_pass:
            errors.addError("No password provided for database")
