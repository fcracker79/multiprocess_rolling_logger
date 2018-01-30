from logging import handlers, LogRecord
import fcntl
import os


def mprolling(supertype, *args, **kwargs):
    class _MP(supertype):
        def __init__(self, *args, **kwargs):
            supertype.__init__(self, *args, **kwargs)
            self.fd = open(self.baseFilename + '__lock__', 'a')
            self.inode = os.stat(self.baseFilename).st_ino

        def emit(self, record):
            fcntl.flock(self.fd, fcntl.LOCK_EX)
            try:
                supertype.emit(self, record)
            finally:
                fcntl.flock(self.fd, fcntl.LOCK_UN)

        def close(self):
            self.fd.close()

    return _MP(*args, **kwargs)


def MPRotatingFileHandler(*args, **kwargs):
    return mprolling(handlers.RotatingFileHandler, *args, **kwargs)


def MPTimedRotatingFileHandler(*args, **kwargs):
    return mprolling(handlers.TimedRotatingFileHandler, *args, **kwargs)
