from typing import List
import numpy as np

from model.target import Target
from model.data_target import DataTarget


class LabelEncoderTarget(Target):
  def __init__(self, source: DataTarget, columns: List[str]):
    super().__init__(sources=[], deps=[source], file_deps=[], cache=False)
    self.source = source
    self.columns = columns


  def execute(self) -> dict:
    label_encoder_dict = {}
    for record in self.source:
      for column in self.columns:
        value = record[column]
        if column in label_encoder_dict:
          label_dict = label_encoder_dict[column]
          if value not in label_dict:
            label_dict[value] = max(label_dict.values()) + np.int_(1)
        else:
          label_encoder_dict[column] = {}
          label_encoder_dict[column][value] = np.int_(0)
    return label_encoder_dict


  def params(self) -> dict:
    return {'columns': self.columns}

