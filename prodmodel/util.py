import logging
import sys
import traceback
from inspect import signature
from pathlib import Path
from typing import GenericMeta, List

import boto3

from prodmodel.globals import TargetConfig, default_config


OUTPUT_FORMAT_TYPES = ('pickle', 'json')


def build_file():
  for stack_frame in traceback.extract_stack():
    if stack_frame.filename.endswith('build.py'):
      return stack_frame
  raise Exception('Could not determine the location of build.py.')


def lib_hash_id() -> str:
  lib_dir = TargetConfig.lib_dir
  if lib_dir is not None:
    assert str(TargetConfig.target_base_dir) in lib_dir and 'lib' in lib_dir, f'Bad lib dir: {lib_dir}'
    return str(Path(lib_dir).name)
  else:
    return ''


class RuleException(Exception):
  pass


class IsolatedSysPath:
  def __init__(self, mod_names: List[str]):
    self.mod_names = mod_names


  def __enter__(self):
    self.original_sys_path = list(sys.path)


  def __exit__(self, pytype, value, traceback):
    for mod_name in self.mod_names:
      if mod_name in sys.modules:
        del sys.modules[mod_name]
    sys.path = self.original_sys_path


class IsolatedModules:
  def __init__(self, source_files: List):
    self.modules = [f.output() for f in source_files]


  def __enter__(self):
    for module in self.modules:
      sys.modules[module.__name__] = module


  def __exit__(self, pytype, value, traceback):
    for module in self.modules:
      del sys.modules[module.__name__]


def red_color(msg: str) -> str:
  return '\033[91m'+ msg + '\033[0m'


def green_color(msg: str) -> str:
  return '\033[92m'+ msg + '\033[0m'


def checkargtypes(fn):
  sign = signature(fn)
  def wrapper_fn(**kwargs):
    def __check(param, arg_type, expected_type):
      if not issubclass(arg_type, expected_type):
        try:
          bf = build_file()
          loc = f'{fn.__name__} at {bf.filename}:{bf.lineno}'
        except Exception as e:
          logging.warning(e)
          loc = ''
        raise RuleException(f'Argument "{param}" has type "{arg_type.__name__}" instead of "{expected_type.__name__}" ({loc}).')
    for param, definition in sign.parameters.items():
      if param in kwargs:
        expected_type = definition.annotation
        arg_type = type(kwargs[param])
        if isinstance(expected_type, GenericMeta) and expected_type.__extra__ == dict:
          __check(param, arg_type, dict)
          if expected_type.__args__:
            for k, v in kwargs[param].items():
              __check(param, type(k), expected_type.__args__[0])
              __check(param, type(v), expected_type.__args__[1])
        elif isinstance(expected_type, GenericMeta) and expected_type.__extra__ == list:
          __check(param, arg_type, list)
          if expected_type.__args__:
            for v in kwargs[param]:
              __check(param, type(v), expected_type.__args__)
        else:
          __check(param, arg_type, expected_type)
    return fn(**kwargs)
  return wrapper_fn


def s3_client():
  return boto3.client(
    's3',
    aws_access_key_id=default_config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=default_config('AWS_SECRET_ACCESS_KEY')
  )
