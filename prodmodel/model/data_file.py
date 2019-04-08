import importlib
import csv

from model.artifact import Artifact


class DataFile(Artifact):

  def __init__(self, file_name: str):
    super().__init__(file_name=file_name)


  def init(self, args):
    self.cached_hash_id = self.hash_id()


  def __iter__(self):
    with open(self.file_name, newline='') as f:
      reader = csv.DictReader(f, delimiter=',')
      return [row for row in reader]
