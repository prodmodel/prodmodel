from prodmodel.model.target import csv_data_target as undertest
from tests.prodmodel.model.target_test_util import TargetTestUtil


class TestCSVDataTarget(TargetTestUtil):

  def test_csv_data_target(self):
    target = undertest.CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str})
    items = [item for item in target]
    self.assertEqual(2, len(items))
    self.assertEqual([{'a': 1, 'b': 'x'}, {'a': 2, 'b': 'y'}], items)
