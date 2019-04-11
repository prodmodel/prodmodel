from typing import Dict
import hashlib

from model.artifact import Artifact, BLOCKSIZE
from model.data_target import DataTarget


class ExternalDataTarget(DataTarget):
  def __init__(self, source: Artifact, fn: str, args: Dict[str, str]):
    super().__init__(sources=[source], deps=[], file_deps=[], cache=False)
    self.source = source
    self.fn = fn
    self.args = args


  def execute(self):
    load_fn = self.source.method(self.fn)
    return load_fn(**self.args)


  def params(self) -> dict:
    return self.args
