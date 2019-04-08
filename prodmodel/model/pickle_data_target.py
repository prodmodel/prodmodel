import pickle

from model.data_target import DataTarget
from model.artifact import Artifact


class PickleDataTarget(DataTarget):
  def __init__(self, source: Artifact):
    super().__init__(sources=[source], deps=[], cache=False)
    self.source = source


  def execute(self):
    with open(self.source.file_name, 'rb') as f:
      return pickle.load(f)
