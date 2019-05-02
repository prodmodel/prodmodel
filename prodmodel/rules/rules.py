from typing import Tuple, List, Dict
from pathlib import Path
import pip._internal
import sys
import os
import hashlib

from model.files.data_file import DataFile
from model.files.external_data_file import ExternalDataFile
from model.target.target import Target
from model.target.data_target import DataTarget
from model.target.iterable_data_target import IterableDataTarget
from model.target.csv_data_target import CSVDataTarget
from model.target.json_data_target import JSONDataTarget
from model.target.binary_data_target import BinaryDataTarget
from model.target.transform_data_target import TransformDataTarget
from model.target.transform_stream_data_target import TransformStreamDataTarget
from model.target.select_data_target import SelectDataTarget
from model.target.sample_data_target import SampleDataTarget
from model.target.label_encoder_target import LabelEncoderTarget
from model.target.encode_label_data_target import EncodeLabelDataTarget
from model.target.test_target import TestTarget
from model.target.external_data_target import ExternalDataTarget
from model.target.pickle_data_target import PickleDataTarget
from model.file_cache import PyFileCache
from util import RuleException, checkargtypes
from globals import TargetConfig


@checkargtypes
def requirements(packages: List[str]):
  '''List of Python packages used by the project.'''

  m = hashlib.sha256()
  for package in packages:
    m.update(package.encode('utf-8'))
  hash_id = m.hexdigest()
  lib_dir = str((TargetConfig.target_base_dir / 'lib' / hash_id).resolve())
  if not os.path.isdir(lib_dir):
    return_value = pip._internal.main(['install', f'--target={lib_dir}', '--ignore-installed'] + packages)
    if return_value > 0:
      raise RuleException('Error happened while installing requirements.')
  sys.path.insert(0, lib_dir)


@checkargtypes
def data_stream(file: str, type: str, dtypes: dict=None) -> IterableDataTarget:
  '''Local data source file. Type has to be one of [csv, json], dtypes is a type specification for the columns in the file.'''

  accepted_types = ('csv', 'json')
  if type not in accepted_types:
    raise RuleException(f'Type must be one of {accepted_types}.')
  if dtypes is not None and type != 'csv':
    raise RuleException(f'Dtypes should only be defined if type is csv.')

  if type == 'csv':
    return CSVDataTarget(DataFile(file), dtypes)
  else: # type == 'json':
    return JSONDataTarget(DataFile(file))


@checkargtypes
def data_file(file: str) -> DataTarget:
  '''Local binary data source file.'''
  return BinaryDataTarget(DataFile(file))


@checkargtypes
def split(data: IterableDataTarget, test_ratio: float, target_column: str, seed: int=0) -> Tuple[IterableDataTarget, IterableDataTarget, IterableDataTarget, IterableDataTarget]:
  '''Splits the source data into train X, train y, test X and test y data, respectively.'''

  train_data = SampleDataTarget(data, 1.0 - test_ratio, seed)
  test_data = SampleDataTarget(data, test_ratio, seed)
  train_x = SelectDataTarget(train_data, [target_column], keep=False)
  train_y = SelectDataTarget(train_data, [target_column], keep=True)
  test_x  = SelectDataTarget(test_data,  [target_column], keep=False)
  test_y  = SelectDataTarget(test_data,  [target_column], keep=True)
  return train_x, train_y, test_x, test_y


@checkargtypes
def transform_stream(file: str, fn: str, stream: IterableDataTarget, objects: Dict[str, DataTarget]={}, file_deps: List[str]=[]) -> IterableDataTarget:
  '''Maps the input data stream into another one. The function `fn` defined in `file` has to accept a dict as a first argument and return a dict.
     The rest of its arguments have to be the keys of `objects` - the outputs of the dict value targets will be substituted at runtime.
     Any module imported in file has to be specified in `file_deps`.'''

  return TransformStreamDataTarget(
    source=PyFileCache.get(file),
    fn=fn,
    stream=stream,
    objects=objects,
    file_deps=[PyFileCache.get(f) for f in file_deps])


@checkargtypes
def transform(file: str, fn: str, streams: Dict[str, IterableDataTarget]={}, objects: Dict[str, DataTarget]={}, file_deps: List[str]=[]) -> DataTarget:
  '''Transforms the input data sets into another one. The function `fn` defined in `file` has to have an argument for every key defined in `streams`
     (list of dicts) and `objects` (the outputs of the dict value targets). Any module imported in file has to be specified in `file_deps`.'''

  return TransformDataTarget(
    source=PyFileCache.get(file),
    fn=fn,
    streams=streams,
    objects=objects,
    file_deps=[PyFileCache.get(f) for f in file_deps])


@checkargtypes
def create_label_encoder(data: IterableDataTarget, columns: List[str]) -> LabelEncoderTarget:
  '''Creates a label encoder from the input `data` stream for the specified `columns`.'''

  return LabelEncoderTarget(data, columns)


@checkargtypes
def encode_labels(data: IterableDataTarget, label_encoder: LabelEncoderTarget) -> IterableDataTarget:
  '''Encodes the label values in `data` with `label_encoder`.'''

  return EncodeLabelDataTarget(data, label_encoder)


@checkargtypes
def test(test_file: str, file_deps: List[str]) -> TestTarget:
  '''Runs the tests in `test_file`. Any module imported in file has to be specified in `file_deps`.'''

  return TestTarget(
    test_file=PyFileCache.get(test_file),
    file_deps=[PyFileCache.get(f) for f in file_deps])


@checkargtypes
def external_data(file: str, fn: str, args: Dict[str, str]) -> DataTarget:
  '''Loads an external dataset by calling `fn` in `file` called with `args`.'''

  external_data_target = ExternalDataTarget(source=PyFileCache.get(file), fn=fn, args=args)
  return PickleDataTarget(ExternalDataFile(external_data_target))
