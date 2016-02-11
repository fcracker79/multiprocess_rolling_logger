import logging
from multiprocessing import Barrier
import os
import tempfile
from unittest import TestCase
from multiprocessing import Process
from mplogger import rolling


class TestRotating(TestCase):
    FILE_SIZE = 20
    FILE_COUNT = 10
    PROCESS_COUNT = 20

    def test(self):
        filename = str(tempfile.mktemp())
        print(filename)

        def process(count: int, barrier: Barrier):
            try:
                logger = logging.Logger('a logger')
                handler = rolling.MPRotatingFileHandler(
                    filename, 'a', self.FILE_SIZE, self.FILE_COUNT
                )
                logger.setLevel(20)
                logger.addHandler(handler)
                logger.info('A nice process: {}'.format(count))
            finally:
                barrier.wait()

        b = Barrier(self.PROCESS_COUNT + 1)
        processes = [Process(target=process, args=(i, b,)) for i in range(self.PROCESS_COUNT)]

        for p in processes:
            p.start()

        b.wait()

        base_filename = os.path.basename(filename)
        count = len([x for x in os.listdir(os.path.dirname(filename)) if base_filename in x])
        self.assertEqual(20, count)
        print('End')
