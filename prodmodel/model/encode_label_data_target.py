import csv

from model.label_encoder_target import LabelEncoderTarget
from model.data_target import DataTarget


class EncodeLabelDataTarget(DataTarget):
  def __init__(self, data: DataTarget, label_encoder: LabelEncoderTarget):
    super().__init__(sources=[], deps=[data, label_encoder], cache=False)
    self.data = data
    self.label_encoder = label_encoder


  def read_record(self) -> dict:
    record = self.data.read_record()
    for column, encoder in self.label_encoder_dict.items():
      record[column] = encoder[record[column]]
    return record


  def init(self):
    self.label_encoder_dict = self.label_encoder.output()


  def finish(self):
    pass
