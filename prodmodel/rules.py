from typing import Tuple, List
from model.target import Target
from model.data_target import DataTarget
from model.csv_data_target import CSVDataTarget
from model.transform_data_target import TransformDataTarget
from model.select_data_target import SelectDataTarget
from model.sample_data_target import SampleDataTarget
from model.label_encoder_target import LabelEncoderTarget
from model.encode_label_data_target import EncodeLabelDataTarget
from model.artifact import Artifact
from model.model_target import ModelTarget
from model.prediction_target import PredictionTarget
from model.evaluation_target import EvaluationTarget


def data_source(file: str, type: str, dtypes: dict, cache: bool=False) -> DataTarget:
  assert type == 'csv'
  return CSVDataTarget(Artifact(file), dtypes, cache)


def split(data: DataTarget, test_ratio: float, target_column: str, seed:int=0) -> Tuple[DataTarget, DataTarget, DataTarget, DataTarget]:
  train_x = SelectDataTarget(SampleDataTarget(data, 1.0 - test_ratio, seed), [target_column], keep=False)
  train_y = SelectDataTarget(SampleDataTarget(data, 1.0 - test_ratio, seed), [target_column], keep=True)
  test_x  = SelectDataTarget(SampleDataTarget(data, test_ratio, seed), [target_column], keep=False)
  test_y  = SelectDataTarget(SampleDataTarget(data, test_ratio, seed), [target_column], keep=True)
  return train_x, train_y, test_x, test_y


def transform(data: DataTarget, file: str, cache: bool=False) -> DataTarget:
  return TransformDataTarget(data, Artifact(file), cache)


def create_label_encoder(data: DataTarget, columns: List[str]) -> LabelEncoderTarget:
  return LabelEncoderTarget(data, columns)


def encode_labels(data: DataTarget, label_encoder: LabelEncoderTarget) -> DataTarget:
  return EncodeLabelDataTarget(data, label_encoder)


def train(features_data: DataTarget, labels_data: DataTarget, file: str) -> ModelTarget:
  return ModelTarget(features_data, labels_data, Artifact(file))


def predict(model: ModelTarget, data: DataTarget, file: str) -> PredictionTarget:
  return PredictionTarget(model, data, Artifact(file))


def evaluate(
  labels_data: DataTarget,
  predictions_data: DataTarget,
  file: str) -> EvaluationTarget:
  return EvaluationTarget(labels_data, predictions_data, Artifact(file))

