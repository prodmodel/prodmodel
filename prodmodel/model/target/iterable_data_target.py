from abc import abstractmethod
import numpy as np
from typing import List

from model.files.input_file import InputFile
from model.target.data_target import DataTarget


class IterableDataTarget(DataTarget):
  def __init__(self, sources: List[InputFile], deps: List[DataTarget], file_deps: List[InputFile]):
    super().__init__(sources=sources, deps=deps, file_deps=file_deps)
    self.sources = sources
    self.deps = deps


  @abstractmethod
  def __iter__(self):
    pass


  def execute(self):
    return np.stack([np.array(list(record.values())) for record in self])
