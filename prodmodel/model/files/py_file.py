import importlib
import time
import shutil
import os
from pathlib import Path

from model.files.input_file import InputFile
from model.files.file_util import build_file
from util import RuleException


class PyFile(InputFile):

  def __init__(self, file_name: str):
    super().__init__(file_name=file_name)
    assert file_name.endswith('.py')
    self.mod = None
    self.cached_build_time = None


  def init_impl(self, args) -> Path:
    self.cached_hash_id = self.hash_id()
    return build_file(args, self)


  def mod_name(self):
      return '.'.join(Path(str(self.relative_name)[:-3]).parts)


  def output(self):
    if self.mod is None or self.cached_hash_id != self.hash_id():
      spec = importlib.util.spec_from_file_location(self.mod_name(), self.file_name)
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      self.mod = mod
    return self.mod


  def method(self, name):
    mod = self.output()
    if name not in dir(mod):
      raise RuleException(f'Method {name} is not found in {self.file_name}.')
    return getattr(mod, name)
