from abc import abstractmethod
import numpy as np
from typing import List

from model.artifact import Artifact
from model.data_target import DataTarget


class IterableDataTarget(DataTarget):
  def __init__(self, sources: List[Artifact], deps: List[DataTarget], file_deps: List[Artifact], cache):
    super().__init__(sources=sources, deps=deps, file_deps=file_deps, cache=cache)
    self.sources = sources
    self.deps = deps


  @abstractmethod
  def __iter__(self):
    pass


  def execute(self):
    return np.stack([np.array(list(record.values())) for record in self])
