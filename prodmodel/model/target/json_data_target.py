import json

from model.files.data_file import DataFile
from model.target.iterable_data_target import IterableDataTarget
from util import RuleException


class JSONDataTarget(IterableDataTarget):
  def __init__(self, source: DataFile):
    super().__init__(sources=[source], deps=[], file_deps=[])
    self.source = source


  def __iter__(self):
    with open(self.source.dest_file_path) as f:
      data = json.load(f)

    if type(data) != list:
      raise RuleException('JSON data must be a JSON array.')

    return data.__iter__()
