import importlib

from model.artifact import Artifact
from model.data_target import DataTarget


class EvaluationTarget(DataTarget):
  def __init__(self, labels_data: DataTarget, predictions_data: DataTarget, source: Artifact):
    super().__init__(sources=[source], deps=[labels_data, predictions_data], cache=False)
    self.source = source
    self.labels_data = labels_data
    self.predictions_data = predictions_data


  def execute(self):
    mod = self.source.output()
    assert 'evaluate' in dir(mod)
    labels_data = self.labels_data.output()
    predictions_data = self.predictions_data.output()
    return mod.evaluate(predicted_y=predictions_data, test_y=labels_data)

