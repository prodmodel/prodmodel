from typing import List

from prodmodel.model.files.input_file import InputFile
from prodmodel.model.target.target import Target


class DataTarget(Target):
  def __init__(self, sources: List[InputFile], deps: List[Target], file_deps: List[InputFile]):
    super().__init__(sources=sources, deps=deps, file_deps=file_deps)
    self.sources = sources
    self.deps = deps
