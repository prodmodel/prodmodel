import random

from model.artifact import Artifact
from model.data_target import DataTarget


class SampleDataTarget(DataTarget):
  def __init__(self, data: DataTarget, ratio: float, seed: int):
    super().__init__(sources=[], deps=[data], cache=False)
    self.data = data
    self.ratio = ratio
    self.seed = seed


  def __iter__(self):
    random.seed(self.seed)
    def sample(record):
      return random.random() < self.ratio
    return filter(sample, self.data.__iter__())


  def init(self):
    pass


  def finish(self):
    pass


  def params(self) -> dict:
    return {'ratio': self.ratio, 'seed': self.seed}

