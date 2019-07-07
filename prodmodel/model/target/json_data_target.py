import json

from prodmodel.model.files.data_file import DataFile
from prodmodel.model.target.iterable_data_target import IterableDataTarget
from prodmodel.util import RuleException


class JSONDataTarget(IterableDataTarget):
  def __init__(self, source: DataFile, output_format: str):
    super().__init__(sources=[source], deps=[], file_deps=[], output_format=output_format)
    self.source = source


  def __iter__(self):
    with open(self.source.dest_file_path) as f:
      data = json.load(f)

    if type(data) != list:
      raise RuleException('JSON data must be a JSON array.')

    return data.__iter__()
