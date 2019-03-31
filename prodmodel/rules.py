from typing import Tuple, List, Dict
from model.target import Target
from model.data_target import DataTarget
from model.iterable_data_target import IterableDataTarget
from model.csv_data_target import CSVDataTarget
from model.transform_data_target import TransformDataTarget
from model.transform_stream_data_target import TransformStreamDataTarget
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


def data_source(file: str, type: str, dtypes: dict, cache: bool=False) -> IterableDataTarget:
  assert type == 'csv'
  return CSVDataTarget(DataFile(file), dtypes, cache)


def split(data: IterableDataTarget, test_ratio: float, target_column: str, seed:int=0) -> Tuple[IterableDataTarget, IterableDataTarget, IterableDataTarget, IterableDataTarget]:
  train_data = SampleDataTarget(data, 1.0 - test_ratio, seed)
  test_data = SampleDataTarget(data, test_ratio, seed)
  train_x = SelectDataTarget(train_data, [target_column], keep=False)
  train_y = SelectDataTarget(train_data, [target_column], keep=True)
  test_x  = SelectDataTarget(test_data,  [target_column], keep=False)
  test_y  = SelectDataTarget(test_data,  [target_column], keep=True)
  return train_x, train_y, test_x, test_y


def transform_stream(stream: IterableDataTarget, file: str, objects: Dict[str, DataTarget]={}, cache: bool=False) -> IterableDataTarget:
  return TransformStreamDataTarget(stream, PyFile(file), objects, cache)


def transform(file: str, streams: Dict[str, IterableDataTarget]={}, objects: Dict[str, DataTarget]={}, cache: bool=False) -> DataTarget:
  return TransformDataTarget(PyFile(file), streams, objects, cache)


def create_label_encoder(data: IterableDataTarget, columns: List[str]) -> LabelEncoderTarget:
  return LabelEncoderTarget(data, columns)


def encode_labels(data: IterableDataTarget, label_encoder: LabelEncoderTarget) -> IterableDataTarget:
  return EncodeLabelDataTarget(data, label_encoder)


def train(features_data: IterableDataTarget, labels_data: IterableDataTarget, file: str) -> ModelTarget:
  return ModelTarget(features_data, labels_data, PyFile(file))


def predict(model: ModelTarget, data: IterableDataTarget, file: str) -> PredictionTarget:
  return PredictionTarget(model, data, PyFile(file))


def evaluate(
  labels_data: IterableDataTarget,
  predictions_data: IterableDataTarget,
  file: str) -> EvaluationTarget:
  return EvaluationTarget(labels_data, predictions_data, PyFile(file))

