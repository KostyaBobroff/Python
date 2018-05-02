import unittest
from files_dict import DirDict
import os
import shutil


class DirDictTest(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dirTest')
        os.mkdir(self.path)
        self.s = DirDict(self.path)
        self.s['alarm'] = 'arm'
        self.s['bar'] = 'Python'
        self.s['foo'] = 'Lkoe'
        self.s['key'] = 'man'

    def test_set_atribute(self):
        path_file = os.path.join(self.path, 'alarm')
        self.assertEqual(True, os.path.exists(path_file))
        with open(path_file, 'r') as f:
            self.assertEqual('arm', f.read().strip())

    def test_get_atribute(self):
        self.assertEqual('Python', self.s['bar'])
        self.assertEqual('arm', self.s['alarm'])
        with self.assertRaises(KeyError):
            self.s['s']

    def test_del_atribute(self):
        path_file = os.path.join(self.path, 'foo')
        del (self.s['foo'])
        self.assertEqual(False, os.path.exists(path_file))
        with self.assertRaises(KeyError):
            del (self.s['arr'])

    def test_len(self):
        self.assertEqual(4, len(self.s))

    def test_iterator(self):
        generator = iter(self.s)
        self.assertEqual('key', next(generator))
        self.assertEqual('foo', next(generator))
        self.assertEqual('alarm', next(generator))
        self.assertEqual('bar', next(generator))

    def tearDown(self):
        shutil.rmtree(self.path)


if __name__ == '__main__':
    unittest.main()
