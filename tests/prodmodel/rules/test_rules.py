import unittest

from prodmodel.rules import rules as undertest


class TestRules(unittest.TestCase):

  def test_data_stream(self):
    target = undertest.data_stream(file='/home/abc/x.json', data_type='json')
    self.assertEqual('JSONDataTarget', target.__class__.__name__)

  def test_data_file(self):
    target = undertest.data_file(file='/home/abc/x.dat')
    self.assertEqual('BinaryDataTarget', target.__class__.__name__)

  def _data_stream(self):
    return undertest.data_stream(file='/home/abc/x.json', data_type='json')

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

  def test_create_label_encoder(self):
    target = undertest.create_label_encoder(data=self._data_stream(), columns=['x'])
    self.assertEqual('LabelEncoderTarget', target.__class__.__name__)

  def test_encode_labels(self):
    le = undertest.create_label_encoder(data=self._data_stream(), columns=['x'])
    target = undertest.encode_labels(data=self._data_stream(), label_encoder=le)
    self.assertEqual('EncodeLabelDataTarget', target.__class__.__name__)

  def test_test(self):
    target = undertest.test(test_file='/home/abc/x.py')
    self.assertEqual('TestTarget', target.__class__.__name__)
