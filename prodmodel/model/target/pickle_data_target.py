import pickle

from prodmodel.model.files.input_file import InputFile
from prodmodel.model.target.data_target import DataTarget


class PickleDataTarget(DataTarget):
  def __init__(self, source: InputFile):
    super().__init__(sources=[source], deps=[], file_deps=[])
    self.source = source


  def execute(self):
    with open(self.source.file_name, 'rb') as f:
      return pickle.load(f)


  def output(self, force=False):
    return self.execute()
