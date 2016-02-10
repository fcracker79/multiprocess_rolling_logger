from logging import handlers, LogRecord
import fcntl

def mprolling(supertype, *args, **kwargs):
    class _MP(supertype):
        def __init__(self, *args, **kwargs):
            supertype.__init__(self, *args, **kwargs)

        def doRollover(self):
            with open(self.baseFilename, 'a') as fd:
                try:
                    fcntl.lockf(fd, fcntl.LOCK_EX)
                    print('DENTRO')
                    if self.shouldRollover(LogRecord(None, None, None, None, None, None, None)):
                        supertype.doRollover(self)
                finally:
                    fcntl.lockf(fd, fcntl.LOCK_UN)
                    print('FUORI')
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