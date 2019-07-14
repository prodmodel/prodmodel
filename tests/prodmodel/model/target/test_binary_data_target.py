import numpy as np

from prodmodel.model.target import binary_data_target as undertest
from tests.prodmodel.model.target_test_util import TargetTestUtil


class TestBinaryDataTarget(TargetTestUtil):

  def test_binary_data_target(self):
    target = undertest.BinaryDataTarget(source=self.csv_data_file)
    output = target.output()
    self.assertEqual(bytes, type(output))
    self.assertEqual(12, len(output))
    self.assertEqual(97, output[0]) # UTF-8 'a' == 97
