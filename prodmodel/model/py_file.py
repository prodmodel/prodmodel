import importlib
from model.artifact import Artifact


class PyFile(Artifact):

  def __init__(self, file_name: str):
    super().__init__(file_name=file_name)
    self.mod = None
    self.current_hash_id = None


  def init(self):
    self.current_hash_id = self.hash_id()


  def output(self):
    if self.mod is None or self.current_hash_id != self.hash_id():
      spec = importlib.util.spec_from_file_location(self.hash_id(), self.file_name)
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      self.mod = mod
    return self.mod

