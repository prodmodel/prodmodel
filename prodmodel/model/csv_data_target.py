import csv

from model.artifact import Artifact
from model.data_target import DataTarget


class CSVDataTarget(DataTarget):
  def __init__(self, source: Artifact, dtypes: dict, cache: bool):
    super().__init__(sources=[source], deps=[], cache=cache)
    self.source = source
    self.dtypes = dtypes
    self.file = None
    self.reader = None


  def read_record(self) -> dict:
    if self.reader is not None:
      record = next(self.reader)
      for k, v in self.dtypes.items():
        record[k] = v(record[k])
      return record


  def init(self):
    self.file = open(self.source.file_name, newline='')
    self.reader = csv.DictReader(self.file, delimiter=',')


  def finish(self):
    if self.file is not None:
      self.file.close()
      self.file = None
    self.reader = None


  def params(self) -> dict:
    return {'dtypes': {k: str(v) for k, v in self.dtypes.items()}}

