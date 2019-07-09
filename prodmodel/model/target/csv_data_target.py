from collections import OrderedDict
import csv

from prodmodel.model.files.data_file import DataFile
from prodmodel.model.target.iterable_data_target import IterableDataTarget


class CSVDataTarget(IterableDataTarget):
  def __init__(self, source: DataFile, dtypes: dict, output_format: str):
    super().__init__(sources=[source], deps=[], file_deps=[], output_format=output_format)
    self.source = source
    self.dtypes = OrderedDict(sorted(dtypes.items()))


  def __iter__(self):
    with open(str(self.source.dest_file_path), newline='') as f:
      reader = csv.DictReader(f, delimiter=',')
      l = [row for row in reader]

    def convert(record):
      output_record = OrderedDict()
      for feature_name, feature_type in self.dtypes.items():
        output_record[feature_name] = feature_type(record[feature_name])
      return output_record
    return map(convert, l.__iter__())


  def params(self) -> dict:
    return {'dtypes': {k: str(v) for k, v in self.dtypes.items()}}
