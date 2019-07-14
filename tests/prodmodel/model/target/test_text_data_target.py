from prodmodel.model.target import text_data_target as undertest
from tests.prodmodel.model.target_test_util import TargetTestUtil


class TestTextDataTarget(TargetTestUtil):

  def test_text_data_target(self):
    target = undertest.TextDataTarget(source=self.csv_data_file)
    output = target.output()
    self.assertEqual(str, type(output))
    self.assertEqual(12, len(output))
    self.assertEqual('a,b\n1,x\n2,y\n', output)
