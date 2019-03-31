import importlib

from model.artifact import Artifact
from model.data_target import DataTarget
from model.model_target import ModelTarget


class PredictionTarget(DataTarget):
  def __init__(self, model: ModelTarget, data: DataTarget, source: Artifact):
    super().__init__(sources=[source], deps=[model, data], cache=False)
    self.source = source
    self.model = model
    self.data = data


  def execute(self):
    predict_fn = self.source.method('predict')
    model = self.model.output()
    data = self.data.output()
    return predict_fn(model=model, records=data)

