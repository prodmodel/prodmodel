import importlib

from model.artifact import Artifact
from model.data_target import DataTarget


class TransformDataTarget(DataTarget):
  def __init__(self, data: DataTarget, source: Artifact, cache: bool):
    super().__init__(sources=[source], deps=[data], cache=cache)
    self.data = data
    self.source = source


  def __iter__(self):
    mod = self.source.output()
    assert 'transform_record' in dir(mod)
    return map(mod.transform_record, self.data.__iter__())


  def init(self):
    pass


  def finish(self):
    pass
