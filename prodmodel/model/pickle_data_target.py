import pickle

from model.data_target import DataTarget
from model.input_file import InputFile


class PickleDataTarget(DataTarget):
  def __init__(self, source: InputFile):
    super().__init__(sources=[source], deps=[], file_deps=[], cache=False)
    self.source = source


  def execute(self):
    with open(self.source.file_name, 'rb') as f:
      return pickle.load(f)


  def output(self, force=False):
    return self.execute()
