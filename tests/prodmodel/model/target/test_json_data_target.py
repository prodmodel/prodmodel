from prodmodel.model.target import json_data_target as undertest
from tests.prodmodel.model.target_test_util import TargetTestUtil


class TestJSONDataTarget(TargetTestUtil):

  def test_json_data_target(self):
    target = undertest.JSONDataTarget(source=self.json_data_file, output_format='pickle')
    items = [item for item in target]
    self.assertEqual(2, len(items))
    self.assertEqual([{'a': 1, 'b': 'x'}, {'a': 2, 'b': 'y'}], items)
