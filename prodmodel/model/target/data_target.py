from abc import abstractmethod
import numpy as np
from typing import List

from model.files.input_file import InputFile
from model.target.target import Target


class DataTarget(Target):
  def __init__(self, sources: List[InputFile], deps: List[Target], file_deps: List[InputFile]):
    super().__init__(sources=sources, deps=deps, file_deps=file_deps)
    self.sources = sources
    self.deps = deps
