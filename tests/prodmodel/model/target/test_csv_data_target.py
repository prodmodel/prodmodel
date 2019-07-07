import numpy as np

from prodmodel.model.target import csv_data_target as undertest
from tests.prodmodel.model.target_test_util import TargetTestUtil


class TestCSVDataTarget(TargetTestUtil):

  def test_csv_data_target(self):
    target = undertest.CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str}, output_format='pickle')
    items = [item for item in target]
    self.assertEqual(2, len(items))
    self.assertEqual([{'a': 1, 'b': 'x'}, {'a': 2, 'b': 'y'}], items)


  def test_csv_data_target__pickle_output_format(self):
    target = undertest.CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str}, output_format='pickle')
    output = target.output()
    self.assertEqual(2, len(output))
    expected = np.stack([np.array(['1', 'x']), np.array(['2', 'y'])])
    self.assertTrue(np.array_equal(expected, output))


  def test_csv_data_target__json_output_format(self):
    target = undertest.CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str}, output_format='json')
    output = target.output()
    self.assertEqual(2, len(output))
    self.assertEqual([{'a': 1, 'b': 'x'}, {'a': 2, 'b': 'y'}], output)
