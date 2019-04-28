from typing import List

from model.target.iterable_data_target import IterableDataTarget


class SelectDataTarget(IterableDataTarget):
  def __init__(self, data: IterableDataTarget, columns: List[str], keep: bool):
    super().__init__(sources=[], deps=[data], file_deps=[])
    self.data = data
    self.columns = columns
    self.keep = keep


  def __iter__(self):
    def select(record):
      if self.keep:
        result = {}
        for column in self.columns:
          result[column] = record[column]
      else:
        result = dict(record)
        for column in self.columns:
          del result[column]
      return result
    return map(select, self.data.__iter__())


  def params(self) -> dict:
    return {'columns': self.columns, 'keep': self.keep}

