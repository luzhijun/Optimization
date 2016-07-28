import sys
PY25 = sys.version_info[0] == 2 and sys.version_info[1] <= 5

from tools import ez_setup, PY25
ez_setup.use_setuptools()
from setuptools import setup, find_packages

__version__ = '0.1a6'

if PY25:
    dependencies = ['simplejson>=3.7.3', ]
else:
    dependencies = []

setup(
    name = 'batchcompute',
    version = __version__,
    description = 'Python SDK for aliyun batchcompute service',
    author = 'BatchCompute Service',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    zip_safe = False,
    license = 'GPL v2.0',
    install_requires = dependencies
)
