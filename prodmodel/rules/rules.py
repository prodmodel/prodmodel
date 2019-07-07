import hashlib
import os
import sys
from typing import Dict, List, Tuple

import pip._internal

from prodmodel.globals import TargetConfig
from prodmodel.model.file_cache import PyFileCache
from prodmodel.model.files.data_file import DataFile
from prodmodel.model.files.external_data_file import ExternalDataFile
from prodmodel.model.files.s3_data_file import S3DataFile
from prodmodel.model.target.binary_data_target import BinaryDataTarget
from prodmodel.model.target.csv_data_target import CSVDataTarget
from prodmodel.model.target.data_target import DataTarget
from prodmodel.model.target.deploy_target import DeployTarget
from prodmodel.model.target.encode_label_data_target import EncodeLabelDataTarget
from prodmodel.model.target.external_data_target import ExternalDataTarget
from prodmodel.model.target.iterable_data_target import IterableDataTarget
from prodmodel.model.target.json_data_target import JSONDataTarget
from prodmodel.model.target.label_encoder_target import LabelEncoderTarget
from prodmodel.model.target.pickle_data_target import PickleDataTarget
from prodmodel.model.target.sample_data_target import SampleDataTarget
from prodmodel.model.target.select_data_target import SelectDataTarget
from prodmodel.model.target.target import Target
from prodmodel.model.target.test_target import TestTarget
from prodmodel.model.target.transform_data_target import TransformDataTarget
from prodmodel.model.target.transform_stream_data_target import TransformStreamDataTarget
from prodmodel.util import OUTPUT_FORMAT_TYPES, RuleException, checkargtypes


def __check_output_format(output_format):
  if output_format not in OUTPUT_FORMAT_TYPES:
    raise RuleException('Invalid output_format, has to be one of {", ".join(OUTPUT_FORMAT_TYPES)}.')



EXTRA_DOC_PARAMS = {
  'output_format': '''The output of the target is specified by `output_format`:<br>
 * `pickle` (default): a numpy array of arrays (serialized with pickle),<br>
 * `json`: a list of dicts (serialzed as JSON).''',
  'file_deps': 'Any local imported module has to be specified in `file_deps`, except for the packages coming from requirements.'
}


@checkargtypes
def requirements(packages: List[str]):
  '''List of Python `packages` used by the project.'''

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
  TargetConfig.lib_dir = lib_dir


def _decode_data_file(file_name):
  if file_name.startswith('s3://'):
    return S3DataFile(file_name)
  else:
    return DataFile(file_name)


@checkargtypes
def data_stream(file: str, data_type: str, dtypes: dict=None, output_format: str='pickle') -> IterableDataTarget:
  '''Local data source `file`; `data_type` has to be one of [csv, json], `dtypes` is a type specification for the columns in the file.'''

  __check_output_format(output_format)
  accepted_types = ('csv', 'json')
  if data_type not in accepted_types:
    raise RuleException(f'Type must be one of {accepted_types}.')
  if dtypes is not None and data_type != 'csv':
    raise RuleException(f'Dtypes should only be defined if type is csv.')

  if data_type == 'csv':
    return CSVDataTarget(_decode_data_file(file), dtypes, output_format)
  else: # type == 'json':
    return JSONDataTarget(_decode_data_file(file), output_format)


@checkargtypes
def data_file(file: str) -> DataTarget:
  '''Local binary data source `file`.'''
  return BinaryDataTarget(_decode_data_file(file))


@checkargtypes
def split(
  data: IterableDataTarget,
  test_ratio: float,
  target_column: str,
  seed: int=0,
  output_format: str='pickle') -> Tuple[IterableDataTarget, IterableDataTarget, IterableDataTarget, IterableDataTarget]:
  '''Splits the source `data` into train X, train y, test X and test y data, respectively. Params:<br>
 * `test_ratio`: [0, 1], the ratio of the test dataset (1 - test_ratio for the train dataset),<br>
 * `target_column`: the name of the target variable included only in the test set,<br>
 * `seed`: random seed for the sampling.'''

  __check_output_format(output_format)
  train_data = SampleDataTarget(data, 1.0 - test_ratio, seed, output_format)
  test_data = SampleDataTarget(data, test_ratio, seed, output_format)
  train_x = SelectDataTarget(train_data, [target_column], keep=False, output_format=output_format)
  train_y = SelectDataTarget(train_data, [target_column], keep=True,  output_format=output_format)
  test_x  = SelectDataTarget(test_data,  [target_column], keep=False, output_format=output_format)
  test_y  = SelectDataTarget(test_data,  [target_column], keep=True,  output_format=output_format)
  return train_x, train_y, test_x, test_y


@checkargtypes
def transform_stream(
  file: str,
  fn: str,
  stream: IterableDataTarget,
  objects: Dict[str, DataTarget]={},
  file_deps: List[str]=[],
  output_format: str='pickle') -> IterableDataTarget:
  '''Maps the input data `stream` into another one. The function `fn` defined in `file` has to accept a dict as a first argument and return a dict.
     The rest of its arguments have to be the keys of `objects` - the outputs of the dict value targets will be substituted at runtime.'''

  __check_output_format(output_format)
  return TransformStreamDataTarget(
    source=PyFileCache.get(file),
    fn=fn,
    stream=stream,
    objects=objects,
    file_deps=[PyFileCache.get(f) for f in file_deps],
    output_format=output_format)


@checkargtypes
def transform(file: str, fn: str, streams: Dict[str, IterableDataTarget]={}, objects: Dict[str, DataTarget]={}, file_deps: List[str]=[]) -> DataTarget:
  '''Transforms the input data sets into another one. The function `fn` defined in `file` has to have an argument for every key defined in `streams`
     (list of dicts) and `objects` (the outputs of the dict value targets).'''

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
def encode_labels(data: IterableDataTarget, label_encoder: LabelEncoderTarget, output_format: str='pickle') -> IterableDataTarget:
  '''Encodes the label values in `data` with `label_encoder`.'''

  __check_output_format(output_format)
  return EncodeLabelDataTarget(data, label_encoder, output_format)


@checkargtypes
def test(test_file: str, file_deps: List[str]=[]) -> TestTarget:
  '''Runs the tests in `test_file`.'''

  return TestTarget(
    test_file=PyFileCache.get(test_file),
    file_deps=[PyFileCache.get(f) for f in file_deps])


@checkargtypes
def external_data(file: str, fn: str, args: Dict[str, str], file_deps: List[str]=[]) -> DataTarget:
  '''Loads an external dataset by calling `fn` in `file` called with `args`.'''

  external_data_target = ExternalDataTarget(
    source=PyFileCache.get(file),
    fn=fn,
    args=args,
    file_deps=[PyFileCache.get(f) for f in file_deps])
  return PickleDataTarget(ExternalDataFile(external_data_target))


@checkargtypes
def deploy_target(data: Target, deploy_path: str) -> DeployTarget:
  '''Deploys the output of `data` to `deploy_path`.'''

  return DeployTarget(data, deploy_path)
