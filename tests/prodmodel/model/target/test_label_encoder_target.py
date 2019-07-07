from prodmodel.model.target import label_encoder_target as undertest
from prodmodel.model.target.csv_data_target import CSVDataTarget
from tests.prodmodel.model.target_test_util import TargetTestUtil


class TestLabelEncoderTarget(TargetTestUtil):

  def test_label_encoder_target(self):
    csv_target = CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str}, output_format='pickle')
    target = undertest.LabelEncoderTarget(csv_target, ['b'])
    self.assertEqual({'b': {'x': 0, 'y': 1}}, target.execute())
