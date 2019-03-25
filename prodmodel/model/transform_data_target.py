import importlib

from model.artifact import Artifact
from model.data_target import DataTarget


class TransformDataTarget(DataTarget):
  def __init__(self, data: DataTarget, source: Artifact, cache: bool):
    super().__init__(sources=[source], deps=[data], cache=cache)
    self.data = data
    self.source = source
    self.mod = None


  def read_record(self) -> dict:
    if self.data is not None and self.mod is not None:
      return self.mod.transform_record(self.data.read_record())


  def init(self):
    spec = importlib.util.spec_from_file_location(self.hash_id(), self.source.file_name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert 'transform_record' in dir(mod)
    self.mod = mod


  def finish(self):
    pass
