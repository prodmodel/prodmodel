from prodmodel.model.target import sample_data_target as undertest
from prodmodel.model.target.csv_data_target import CSVDataTarget
from tests.prodmodel.model.target_test_util import TargetTestUtil


class TestSampleDataTarget(TargetTestUtil):

  def test_sample_data_target(self):
    csv_target = CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str}, output_format='pickle')
    target = undertest.SampleDataTarget(csv_target, ratio=0.5, seed=1, output_format='pickle')
    items = [item for item in target]
    self.assertEqual(1, len(items))
    self.assertEqual([{'a': 1, 'b': 'x'}], items)
