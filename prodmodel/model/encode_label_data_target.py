import csv

from model.label_encoder_target import LabelEncoderTarget
from model.iterable_data_target import IterableDataTarget


class EncodeLabelDataTarget(IterableDataTarget):
  def __init__(self, data: IterableDataTarget, label_encoder: LabelEncoderTarget):
    super().__init__(sources=[], deps=[data, label_encoder], cache=False)
    self.data = data
    self.label_encoder = label_encoder


  def __iter__(self):
    self.label_encoder_dict = self.label_encoder.output()
    def encode(record):
      for column, encoder in self.label_encoder_dict.items():
        record[column] = encoder[record[column]]
      return record
    return map(encode, self.data.__iter__())


  def init(self):
    pass


  def finish(self):
    pass
