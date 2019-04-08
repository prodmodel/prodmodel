import importlib
from model.artifact import Artifact
from util import RuleException
import time


class PyFile(Artifact):

  def __init__(self, file_name: str):
    super().__init__(file_name=file_name)
    self.mod = None
    self.current_hash_id = None
    self.current_build_time = None


  def init(self, args):
    if self.current_build_time != args.build_time:
      self.current_hash_id = self.hash_id()
      self.current_build_time = args.build_time


  def output(self):
    if self.mod is None or self.current_hash_id != self.hash_id():
      spec = importlib.util.spec_from_file_location(self.hash_id(), self.file_name)
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      self.mod = mod
    return self.mod


  def method(self, name):
    mod = self.output()
    if name not in dir(mod):
      raise RuleException(f'Method {name} is not found in {self.file_name}.')
    return getattr(mod, name)
