from tests.prodmodel.model.target_test_util import TargetTestUtil
from prodmodel.model.target.csv_data_target import CSVDataTarget
from prodmodel.model.target.label_encoder_target import LabelEncoderTarget
from prodmodel.model.target import encode_label_data_target as undertest


class TestEncodeLabelsDataTarget(TargetTestUtil):

  def test_label_encoder_target(self):
    csv_target = CSVDataTarget(source=self.csv_data_file, dtypes={'a': int, 'b': str})
    label_encoder = LabelEncoderTarget(csv_target, ['b'])
    target = undertest.EncodeLabelDataTarget(csv_target, label_encoder)
    items = [item for item in target]
    self.assertEqual(2, len(items))
    self.assertEqual([{'a': 1, 'b': 0}, {'a': 2, 'b': 1}], items)
