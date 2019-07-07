from abc import abstractmethod
from typing import List

import numpy as np

from prodmodel.model.files.input_file import InputFile
from prodmodel.model.target.data_target import DataTarget
from prodmodel.util import OUTPUT_FORMAT_TYPES


class IterableDataTarget(DataTarget):
  def __init__(self, sources: List[InputFile], deps: List[DataTarget], file_deps: List[InputFile], output_format: str):
    super().__init__(sources=sources, deps=deps, file_deps=file_deps)
    self.sources = sources
    self.deps = deps
    assert output_format in OUTPUT_FORMAT_TYPES
    self.output_format = output_format


  @abstractmethod
  def __iter__(self):
    pass


  def execute(self):
    if self.output_format == 'pickle':
      return np.stack([np.array(list(record.values())) for record in self])
    else:
      return [record for record in self]
