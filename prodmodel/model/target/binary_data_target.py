from prodmodel.model.files.data_file import DataFile
from prodmodel.model.target.data_target import DataTarget


class BinaryDataTarget(DataTarget):
  def __init__(self, source: DataFile):
    super().__init__(sources=[source], deps=[], file_deps=[])
    self.source = source


  def execute(self):
    with open(self.source.dest_file_path) as f:
      return f.read()
