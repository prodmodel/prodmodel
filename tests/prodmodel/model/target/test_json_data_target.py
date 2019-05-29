from tests.prodmodel.model.target_test_util import TargetTestUtil
from prodmodel.model.target import json_data_target as undertest


class TestJSONDataTarget(TargetTestUtil):

  def test_json_data_target(self):
    target = undertest.JSONDataTarget(source=self.data_file)
    items = [item for item in target]
    self.assertEqual(2, len(items))
    self.assertEqual([{'a': 1, 'b': 'x'}, {'a': 2, 'b': 'y'}], items)
