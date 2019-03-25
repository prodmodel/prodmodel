import importlib

from model.target import Target
from model.artifact import Artifact
from model.data_target import DataTarget


class ModelTarget(Target):
  def __init__(self, features_data: DataTarget, labels_data: DataTarget, source: Artifact):
    super().__init__(sources=[source], deps=[features_data, labels_data], cache=True)
    self.features_data = features_data
    self.labels_data = labels_data
    self.source = source


  def execute(self):
    spec = importlib.util.spec_from_file_location(self.hash_id(), self.source.file_name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert 'train' in dir(mod)
    X = self.features_data.output()
    y = self.labels_data.output()
    return mod.train(X=X, y=y)

