from abc import abstractmethod
import numpy as np
from typing import List

from model.artifact import Artifact
from model.data_target import DataTarget


class IterableDataTarget(DataTarget):
  def __init__(self, sources: List[Artifact], deps: List[DataTarget], cache):
    super().__init__(sources=sources, deps=deps, cache=cache)
    self.sources = sources
    self.deps = deps


  @abstractmethod
  def __iter__(self):
    pass


  def execute(self):
    return np.stack([np.fromiter(record.values(), dtype=float) for record in self])
