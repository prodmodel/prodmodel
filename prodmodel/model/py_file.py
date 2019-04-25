import importlib
from model.input_file import InputFile
from util import RuleException
import time
from pathlib import Path


class PyFile(InputFile):

  def __init__(self, file_name: str):
    super().__init__(file_name=file_name)
    assert file_name.endswith('.py')
    self.mod = None
    self.cashed_build_time = None


  def init(self, args):
    if self.cashed_build_time != args.build_time:
      self.cached_hash_id = self.hash_id()
      self.cashed_build_time = args.build_time


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
