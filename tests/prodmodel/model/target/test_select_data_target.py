from prodmodel.model.target import select_data_target as undertest
from prodmodel.model.target.csv_data_target import CSVDataTarget
from tests.prodmodel.model.target_test_util import TargetTestUtil


class TestSelectDataTarget(TargetTestUtil):

  def test_select_data_target__keep(self):
    csv_target = CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str})
    target = undertest.SelectDataTarget(csv_target, ['a'], keep=True)
    items = [item for item in target]
    self.assertEqual(2, len(items))
    self.assertEqual([{'a': 1}, {'a': 2}], items)


  def test_select_data_target__discard(self):
    csv_target = CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str})
    target = undertest.SelectDataTarget(csv_target, ['a'], keep=False)
    items = [item for item in target]
    self.assertEqual(2, len(items))
    self.assertEqual([{'b': 'x'}, {'b': 'y'}], items)
