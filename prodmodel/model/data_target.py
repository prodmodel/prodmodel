from abc import abstractmethod
import numpy as np
from typing import List

from model.artifact import Artifact
from model.target import Target


class DataTarget(Target):
  def __init__(self, sources: List[Artifact], deps: List[Target], file_deps: List[Artifact], cache):
    super().__init__(sources=sources, deps=deps, file_deps=file_deps, cache=cache)
    self.sources = sources
    self.deps = deps
