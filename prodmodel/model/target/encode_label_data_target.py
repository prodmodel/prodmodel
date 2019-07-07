from prodmodel.model.target.iterable_data_target import IterableDataTarget
from prodmodel.model.target.label_encoder_target import LabelEncoderTarget


class EncodeLabelDataTarget(IterableDataTarget):
  def __init__(self, data: IterableDataTarget, label_encoder: LabelEncoderTarget, output_format: str):
    super().__init__(sources=[], deps=[data, label_encoder], file_deps=[], output_format=output_format)
    self.data = data
    self.label_encoder = label_encoder


  def __iter__(self):
    self.label_encoder_dict = self.label_encoder.output()
    def encode(record):
      for column, encoder in self.label_encoder_dict.items():
        record[column] = encoder[record[column]]
      return record
    return map(encode, self.data.__iter__())
