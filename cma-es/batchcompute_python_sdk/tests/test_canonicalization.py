import os
import sys
sys.path.append('../../')
import copy
import unittest

from batchcompute.utils.functions import timestamp_datetime, timediff
from batchcompute.utils.canonicalization import remap

class TestCanonicalization(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_remap(self):
        # test job_id remap.
        job_id = 'job-xxxx'
        d = {
            'ResourceId': job_id
        }
        remapped = remap(d)
        self.assertTrue('ResourceId' not in d)
        self.assertEqual(remapped['JobId'], job_id)

        # test img_id remap.
        img_id = 'img-xxxx'
        d = {
            'ResourceId': img_id
        }
        remapped = remap(d)
        self.assertTrue('ResourceId' not in d)
        self.assertEqual(remapped['ImageId'], img_id)

        # test state remap.
        state = 'Terminated'
        d = {
            'State': state
        }
        remapped = remap(d)
        self.assertEqual(remapped['State'], 'Finished')

        # test error_code remap.
        code = 400
        d = {
            'ErrorCode': code
        }
        remapped = remap(d)
        self.assertTrue('ErrorCode' not in remapped)
        self.assertEqual(remapped['Code'], code)

        # test error_code remap.
        instance_status_list = [1, 2, 3, 4]
        d = {
            'InstanceStatusVector': instance_status_list
        }
        remapped = remap(d)
        self.assertTrue('InstanceStatusVector' not in remapped)
        self.assertEqual(remapped['InstanceList'], instance_status_list)

        # test human readable time format.
        int_time = 1437116316
        total_time = 0
        d = {
            'StartTime': int_time,
            'EndTime': int_time,
            'TotalTime': 0
        }

        remapped = remap(d, False)
        self.assertEqual(remapped['StartTime'], int_time)
        self.assertEqual(remapped['EndTime'], int_time)
        self.assertEqual(remapped['TotalTime'], total_time)

        remapped = remap(d, True)
        self.assertEqual(remapped['StartTime'], timestamp_datetime(int_time))
        self.assertEqual(remapped['EndTime'], timestamp_datetime(int_time))
        self.assertEqual(remapped['TotalTime'], timediff(total_time))

        # test add task name.
        d = {
            'Find': {
                'UnfinishedInstances': [1, 2, 3, 4]
            }
        }
        remapped = remap(d)
        self.assertTrue('TaskName' in remapped['Find'])


if __name__ == '__main__':
    unittest.main()
