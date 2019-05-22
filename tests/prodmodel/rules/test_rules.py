import unittest
from prodmodel.rules import rules as undertest


class TestRules(unittest.TestCase):

  def test_data_stream(self):
    target = undertest.data_stream(file='/home/abc/x.json', type='json')
    self.assertEqual('JSONDataTarget', target.__class__.__name__)

  def test_data_file(self):
    target = undertest.data_file(file='/home/abc/x.dat')
    self.assertEqual('BinaryDataTarget', target.__class__.__name__)

  def _data_stream(self):
    return undertest.data_stream(file='/home/abc/x.json', type='json')

  def test_split(self):
    train_x, train_y, test_x, test_y = undertest.split(data=self._data_stream(), test_ratio=0.5, target_column='x')
    self.assertEqual('SelectDataTarget', train_x.__class__.__name__)
    self.assertEqual('SelectDataTarget', train_y.__class__.__name__)
    self.assertEqual('SelectDataTarget', test_x.__class__.__name__)
    self.assertEqual('SelectDataTarget', test_y.__class__.__name__)

  def test_transform_stream(self):
    target = undertest.transform_stream(file='/home/abc/x.py', fn='tf', stream=self._data_stream())
    self.assertEqual('TransformStreamDataTarget', target.__class__.__name__)

  def test_transform(self):
    target = undertest.transform(file='/home/abc/x.py', fn='tf', streams={'s': self._data_stream()})
    self.assertEqual('TransformDataTarget', target.__class__.__name__)
