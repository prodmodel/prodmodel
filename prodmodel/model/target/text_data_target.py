from prodmodel.model.files.data_file import DataFile
from prodmodel.model.target.data_target import DataTarget


class TextDataTarget(DataTarget):
  def __init__(self, source: DataFile):
    super().__init__(sources=[source], deps=[], file_deps=[])
    self.source = source


  def execute(self):
    with open(str(self.source.dest_file_path), mode='r') as f:
      return f.read()
