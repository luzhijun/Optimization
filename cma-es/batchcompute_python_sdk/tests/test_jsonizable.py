import os
import sys
sys.path.append('../../')
import copy
import unittest

from batchcompute.utils.jsonizable import Jsonizable
from batchcompute.utils.functions import import_json
from batchcompute.utils.constants import STRING 

json = import_json()

class DummyJson(Jsonizable):
    descriptor_type = 'data descriptor'
    descriptor_map = {
        'Property_1': int,
        'Property_2': STRING,
        'Property_3': list
    }

    def __init__(self, properties={}):
        super(DummyJson, self).__init__(properties)

class DummyJson2(Jsonizable):
    descriptor_type = 'non data descriptor'
    descriptor_map = {
        'Property_1': int,
        'Property_2': STRING, 
        'Property_3': list
    }

    def __init__(self, properties={}):
        super(DummyJson2, self).__init__(properties)

class JsonizableTest(unittest.TestCase):

    def setUp(self):
        self.property_1 = 1
        self.property_2 = 'batchcompute test'
        self.property_3 = [1,2,3,4]

    def tearDown(self):
        pass

    def test_init(self):
        def get_all_properties(obj):
            self.assertEqual(obj.Property_1, self.property_1)
            self.assertEqual(obj.Property_2, self.property_2)
            self.assertEqual(obj.Property_3, self.property_3)

            self.assertEqual(obj['Property_1'], self.property_1)
            self.assertEqual(obj['Property_2'], self.property_2)
            self.assertEqual(obj['Property_3'], self.property_3)

        # test init through a dict.
        properties = {
            'Property_1': self.property_1,
            'Property_2': self.property_2,
            'Property_3': self.property_3
        }

        j = DummyJson(properties)
        get_all_properties(j)

        # test init through a json string.
        properties = '''{
            "Property_1": %s,
            "Property_2": "%s",
            "Property_3": %s
        }''' % (self.property_1, self.property_2, self.property_3)

        j = DummyJson(properties)
        get_all_properties(j)

        j2 = DummyJson(j)
        get_all_properties(j2)

        # test init througn assigning properties one by one.
        j = DummyJson()
        j.Property_1 = self.property_1
        j.Property_2 = self.property_2
        j.Property_3 = self.property_3
        get_all_properties(j)

    def test_update(self):
        properties = {
            'Property_1': self.property_1,
            'Property_2': self.property_2,
            'Property_4': self.property_3
        }
        j = DummyJson()
        j.update(properties)
        self.assertEqual(j.Property_1, self.property_1)
        self.assertEqual(j.Property_2, self.property_2)

    def test_load(self):
        properties = '''{
            "Property_1": %s,
            "Property_2": "%s"
        }''' % (self.property_1, self.property_2)
        j = DummyJson()
        j.load(properties)
        self.assertEqual(j.Property_1, self.property_1)
        self.assertEqual(j.Property_2, self.property_2)
        self.assertEqual(j.Property_3, None)

    def test_dump(self):
        properties = {
            'Property_1': self.property_1,
            'Property_2': self.property_2,
            'Property_3': self.property_3
        }
        j = DummyJson(properties)
        self.assertEqual(j.dump(), json.dumps(properties, indent=4))

    def test_invalid_property(self):
        properties = {
            'Property_1': self.property_1,
            'Property_2': self.property_2,
            'Property_3': self.property_3
        }
        j = DummyJson(properties)

        # test invalid properties
        def get_property_by_index(obj, property_name):
            return j[property_name]
        def get_property_by_name(obj, property_name):
            return getattr(obj, property_name)
        self.assertRaises(KeyError, get_property_by_index, j, 'Property_4')
        self.assertRaises(AttributeError, get_property_by_name, j, 'Property_4')

    def test_invalid_setter(self):
        properties = {
            'Property_1': self.property_1,
            'Property_2': self.property_2,
            'Property_3': self.property_3
        }

        j= DummyJson2(properties)

        def set_property(obj, name, value):
            setattr(obj, name, value)
        self.assertRaises(AttributeError, set_property, j, 'Property_1', self.property_1)
        self.assertRaises(AttributeError, set_property, j, 'Property_2', self.property_2)
        self.assertRaises(AttributeError, set_property, j, 'Property_3', self.property_3)

    def test_copy(self):
        properties = {
            'Property_1': self.property_1,
            'Property_2': self.property_2,
            'Property_3': self.property_3
        }

        j = DummyJson(properties)

        j2 = copy.deepcopy(j)
        j2.Property_1 = self.property_1 + 1
        self.assertEqual(j.Property_1, self.property_1)
        self.assertEqual(j2.Property_1, self.property_1 + 1)


if __name__ == '__main__':
    unittest.main()
