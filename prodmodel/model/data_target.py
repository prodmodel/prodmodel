from abc import abstractmethod
import numpy as np
from typing import List

from model.artifact import Artifact
from model.target import Target


class DataTarget(Target):
  def __init__(self, sources: List[Artifact], deps: List[Target], cache):
    super().__init__(sources=sources, deps=deps, cache=cache)
    self.sources = sources
    self.deps = deps


  @abstractmethod
  def read_record(self) -> dict:
    pass


  def __iter__(self):
    return self


  def __next__(self):
     return self.read_record()


  def execute(self):
    self.init_with_deps()
    array = np.stack([np.fromiter(record.values(), dtype=float) for record in self])
    self.finish_with_deps()
    return array

