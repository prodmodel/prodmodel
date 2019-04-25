import importlib
import csv
import shutil
from pathlib import Path
from globals import TargetConfig


from model.input_file import InputFile


class DataFile(InputFile):

  def __init__(self, file_name: str):
    super().__init__(file_name=file_name)
    self.cashed_build_time = None


  def init(self, args):
    if self.cashed_build_time != args.build_time:
      self.cashed_build_time = args.build_time
      self.cached_hash_id = self.hash_id()
      if args.cache_data:
        path = TargetConfig.target_base_dir / 'data' / self.relative_name / self.cached_hash_id
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.is_file():
          shutil.copy(self.file_name, path)


  def __iter__(self):
    with open(self.file_name, newline='') as f:
      reader = csv.DictReader(f, delimiter=',')
      return [row for row in reader]
