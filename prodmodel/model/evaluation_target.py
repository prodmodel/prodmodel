import importlib

from model.artifact import Artifact
from model.target import Target
from model.iterable_data_target import IterableDataTarget


class EvaluationTarget(Target):
  def __init__(self, labels_data: IterableDataTarget, predictions_data: IterableDataTarget, source: Artifact):
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

