from tests.prodmodel.model.target_test_util import TargetTestUtil
from prodmodel.model.target.csv_data_target import CSVDataTarget
from prodmodel.model.target import transform_stream_data_target as undertest


class TestTransformStreamDataTarget(TargetTestUtil):

  def test_select_data_target__keep(self):
    csv_target = CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str})
    target = undertest.TransformStreamDataTarget(self.py_file, 'a_plus_1', csv_target, objects={}, file_deps=[])
    items = [item for item in target]
    self.assertEqual(2, len(items))
    self.assertEqual([{'a': 2}, {'a': 3}], items)