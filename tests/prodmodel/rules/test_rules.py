import unittest
from prodmodel.rules import rules as undertest


class TestRules(unittest.TestCase):

  def test_data_stream(self):
    target = undertest.data_stream(file='/home/abc/x.json', type='json')
    self.assertEqual('JSONDataTarget', target.__class__.__name__)

