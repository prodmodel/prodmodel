from typing import Tuple, List
from model.target import Target
from model.data_target import DataTarget
from model.csv_data_target import CSVDataTarget
from model.transform_data_target import TransformDataTarget
from model.select_data_target import SelectDataTarget
from model.sample_data_target import SampleDataTarget
from model.label_encoder_target import LabelEncoderTarget
from model.encode_label_data_target import EncodeLabelDataTarget
from model.data_file import DataFile
from model.py_file import PyFile
from model.model_target import ModelTarget
from model.prediction_target import PredictionTarget
from model.evaluation_target import EvaluationTarget
from pathlib import Path
import pip._internal
import sys
import os
import hashlib


class RuleException(Exception):
  pass


def requirements(packages: List[str]):
  m = hashlib.sha256()
  for package in packages:
    m.update(package.encode('utf-8'))
  hash_id = m.hexdigest()
  lib_dir = str((Path('target') / 'lib' / hash_id).resolve())
  if not os.path.isdir(lib_dir):
    return_value = pip._internal.main(['install', f'--target={lib_dir}', '--ignore-installed'] + packages)
    if return_value > 0:
      raise RuleException('Error happened while installing requirements.')
  sys.path.insert(0, lib_dir)


def data_source(file: str, type: str, dtypes: dict, cache: bool=False) -> DataTarget:
  assert type == 'csv'
  return CSVDataTarget(DataFile(file), dtypes, cache)


def split(data: DataTarget, test_ratio: float, target_column: str, seed:int=0) -> Tuple[DataTarget, DataTarget, DataTarget, DataTarget]:
  train_data = SampleDataTarget(data, 1.0 - test_ratio, seed)
  test_data = SampleDataTarget(data, test_ratio, seed)
  train_x = SelectDataTarget(train_data, [target_column], keep=False)
  train_y = SelectDataTarget(train_data, [target_column], keep=True)
  test_x  = SelectDataTarget(test_data,  [target_column], keep=False)
  test_y  = SelectDataTarget(test_data,  [target_column], keep=True)
  return train_x, train_y, test_x, test_y


def transform(data: DataTarget, file: str, cache: bool=False) -> DataTarget:
  return TransformDataTarget(data, PyFile(file), cache)


def create_label_encoder(data: DataTarget, columns: List[str]) -> LabelEncoderTarget:
  return LabelEncoderTarget(data, columns)


def encode_labels(data: DataTarget, label_encoder: LabelEncoderTarget) -> DataTarget:
  return EncodeLabelDataTarget(data, label_encoder)


def train(features_data: DataTarget, labels_data: DataTarget, file: str) -> ModelTarget:
  return ModelTarget(features_data, labels_data, PyFile(file))


def predict(model: ModelTarget, data: DataTarget, file: str) -> PredictionTarget:
  return PredictionTarget(model, data, PyFile(file))


def evaluate(
  labels_data: DataTarget,
  predictions_data: DataTarget,
  file: str) -> EvaluationTarget:
  return EvaluationTarget(labels_data, predictions_data, PyFile(file))

