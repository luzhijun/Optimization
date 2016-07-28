import os
import sys
sys.path.append('../../')
import copy
import unittest

from batchcompute import CN_QINGDAO
from batchcompute.utils.jsonizable import Jsonizable
from batchcompute.utils.functions import (
    import_json, import_httplib, iget, get_region, ConfigError, timediff,
)

json = import_json()
httplib = import_httplib()

class TestFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_iget(self):
        d = {
            'GetTest': 'Just for test',
        }

        self.assertEqual(iget(d, 'GetTest'), iget(d, 'getTest'))
        self.assertEqual(iget(d, 'Gettest'), iget(d, 'getTest'))
        self.assertEqual(iget(d, 'GeTTest'), iget(d, 'getTest'))

    def test_get_region(self):
        err_endpoint = CN_QINGDAO + 'err'
        self.assertRaises(ConfigError, get_region, err_endpoint)

    def test_timediff(self):
        self.assertEqual('0', timediff(0))
        # second.
        self.assertEqual('1 Second', timediff(1))
        self.assertEqual('2 Seconds', timediff(2))
        # minute.
        self.assertEqual('1 Minute', timediff(60))
        self.assertEqual('2 Minutes', timediff(2*60))
        # hour.
        self.assertEqual('1 Hour', timediff(3600))
        self.assertEqual('2 Hours', timediff(2*3600))
        # day.
        self.assertEqual('1 Day', timediff(86400))
        self.assertEqual('2 Days', timediff(2*86400))

        self.assertEqual('1 Day 1 Second', timediff(86401))
        self.assertEqual('1 Day 2 Seconds', timediff(86402))


if __name__ == '__main__':
    unittest.main()
