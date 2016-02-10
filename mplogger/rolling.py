from logging import handlers, LogRecord
import fcntl
import os
import sys


def mprolling(supertype, *args, **kwargs):
    class _MP(supertype):
        def __init__(self, *args, **kwargs):
            supertype.__init__(self, *args, **kwargs)
            self.fd = open(self.baseFilename + '__lock__', 'a')

        def doRollover(self):
            try:
                fcntl.flock(self.fd, fcntl.LOCK_EX)
                print('DENTRO{}'.format(os.getpid()))
                sys.stdout.flush()
                if self.shouldRollover(LogRecord(None, None, None, None, None, None, None)):
                    print('\tROLLOVER{}'.format(os.getpid()))
                    sys.stdout.flush()
                    print('\tROLLOVER END{}'.format(os.getpid()))
                    supertype.doRollover(self)
            finally:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
                print('FUORI{}'.format(os.getpid()))
                sys.stdout.flush()

        def close(self):
            self.fd.close()

    return _MP(*args, **kwargs)

def MPRotatingFileHandler(*args, **kwargs):
    return mprolling(handlers.RotatingFileHandler, *args, **kwargs)

def MPTimedRotatingFileHandler(*args, **kwargs):
    return mprolling(handlers.TimedRotatingFileHandler, *args, **kwargs)

"""
class MPRotatingFileHandler(handlers.RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        handlers.RotatingFileHandler.__init__(*args, **kwargs)

    def doRollover(self):
        with open(self.baseFilename, 'a') as fd:
            try:
                fcntl.lockf(fd, fcntl.LOCK_EX)
                if self.shouldRollover(''):
                    handlers.RotatingFileHandler.doRollover(self)
            finally:
                fcntl.lockf(fd, fcntl.LOCK_UN)

class MPTimeRotatingFileHandler(handlers.TimedRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        handlers.TimedRotatingFileHandler.__init__(*args, **kwargs)

    def doRollover(self):
        with open(self.baseFilename, 'a') as fd:
            try:
                fcntl.lockf(fd, fcntl.LOCK_EX)
                if self.shouldRollover(''):
                    handlers.TimedRotatingFileHandler.doRollover(self)
            finally:
                fcntl.lockf(fd, fcntl.LOCK_UN)
"""