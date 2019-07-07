import random

from prodmodel.model.target.iterable_data_target import IterableDataTarget


class SampleDataTarget(IterableDataTarget):
  def __init__(self, data: IterableDataTarget, ratio: float, seed: int, output_format: str):
    super().__init__(sources=[], deps=[data], file_deps=[], output_format=output_format)
    self.data = data
    self.ratio = ratio
    self.seed = seed


  def __iter__(self):
    random.seed(self.seed)
    def sample(record):
      return random.random() < self.ratio
    return filter(sample, self.data.__iter__())


  def params(self) -> dict:
    return {'ratio': self.ratio, 'seed': self.seed}
