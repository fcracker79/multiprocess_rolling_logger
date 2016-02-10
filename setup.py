import os
import sys

from setuptools import setup, find_packages

major, minor1, minor2, release, serial = sys.version_info

readfile_kwargs = {"encoding": "utf-8"} if major >= 3 else {}

def readfile(filename):
    with open(filename, **readfile_kwargs) as fp:
        contents = fp.read()
    return contents

def get_packages(path):
    out = [path]
    for x in find_packages(path):
        out.append('{}/{}'.format(path, x))
    
    return out

packages = get_packages('mplogger')

requirements = readfile(os.path.join(os.path.dirname(__file__), "requirements.txt"))

setup(name='mplogger',
      version='0.0.1',
      description='Multi processing logging module',
      url='https://github.com/fcracker79/multiprocess_rolling_logger',
      author='fcracker79@gmail.com',
      author_email='fcracker79@gmail.com',
      license='MIT',
      packages=packages,
      install_requires=requirements,
      zip_safe=False,
      test_suite="test")
