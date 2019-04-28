import importlib
import csv
import shutil
import os
from pathlib import Path

from model.files.input_file import InputFile
from model.files.file_util import build_file


class DataFile(InputFile):

  def __init__(self, file_name: str):
    super().__init__(file_name=file_name)
    self.cached_build_time = None


  def init_impl(self, args) -> Path:
    self.cached_hash_id = self.hash_id()
    return build_file(args, self)


  def __iter__(self):
    with open(self.file_name, newline='') as f:
      reader = csv.DictReader(f, delimiter=',')
      return [row for row in reader]
