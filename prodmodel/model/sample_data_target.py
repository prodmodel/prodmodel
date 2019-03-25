import random

from model.artifact import Artifact
from model.data_target import DataTarget


class SampleDataTarget(DataTarget):
  def __init__(self, data: DataTarget, ratio: float, seed: int):
    super().__init__(sources=[], deps=[data], cache=False)
    self.data = data
    self.ratio = ratio
    self.seed = seed


  def read_record(self) -> dict:
    if self.data is not None:
      while True:
        record = self.data.read_record()
        if random.random() < self.ratio:
          break
      return record


  def init(self):
    random.seed(self.seed)
    pass


  def finish(self):
    pass


  def params(self) -> dict:
    return {'ratio': self.ratio, 'seed': self.seed}

