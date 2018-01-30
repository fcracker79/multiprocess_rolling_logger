import logging
from multiprocessing import Barrier
import os
import tempfile
from time import sleep
from unittest import TestCase
from multiprocessing import Process

from mplogger import rolling


def _file_len(fname):
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


class TestRotating(TestCase):
    FILE_SIZE = 20
    FILE_COUNT = 200
    PROCESS_COUNT = 300

    def test(self):
        filename = str(tempfile.mktemp())

        def process(cur_count: int, barrier: Barrier):
            try:
                logger = logging.Logger('a logger')
                handler = rolling.MPRotatingFileHandler(
                    filename, 'a', self.FILE_SIZE, self.FILE_COUNT
                )
                logger.setLevel(20)
                logger.addHandler(handler)
                sleep(1)  # This is just to simulate presence of handlers
                s = 'Proc {}, Pid {}'.format(cur_count, os.getpid())
                s += '*' * (self.FILE_SIZE - len(s) - 2)
                logger.info(s)
            finally:
                barrier.wait()

        b = Barrier(self.PROCESS_COUNT + 1)
        processes = [Process(target=process, args=(i, b,)) for i in range(self.PROCESS_COUNT)]

        for p in processes:
            p.start()

        b.wait()

        base_filename = os.path.basename(filename)
        count = sum([_file_len('{}/{}'.format(os.path.dirname(filename), x))
                     for x in os.listdir(os.path.dirname(filename)) if base_filename in x]) - 1
        self.assertEqual(self.FILE_COUNT + 1, count)
