from tests.prodmodel.model.target_test_util import TargetTestUtil
from prodmodel.model.target.csv_data_target import CSVDataTarget
from prodmodel.model.target import transform_data_target as undertest


class TestTransformDataTarget(TargetTestUtil):

  def test_select_data_target__keep(self):
    csv_target = CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str})
    target = undertest.TransformDataTarget(self.py_file, 'csv_length', streams={}, objects={'csv': csv_target}, file_deps=[])
    self.assertEqual(2, target.execute())
