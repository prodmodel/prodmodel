import traceback
import sys
from pathlib import Path
from inspect import signature
from typing import List, Dict, GenericMeta


def build_file():
  for stack_frame in traceback.extract_stack():
    if stack_frame.filename.endswith('build.py'):
      return stack_frame


def lib_hash_id():
  lib_dir = sys.path[0]
  assert 'target' in lib_dir and 'lib' in lib_dir 
  return str(Path(lib_dir).name)


class RuleException(Exception):
  pass


class IsolatedSysPath:
  def __enter__(self):
    self.original_sys_path = list(sys.path)

  def __exit__(self, type, value, traceback):
    sys.path = self.original_sys_path


def red_color(msg: str) -> str:
  return '\033[91m'+ msg + '\033[0m'


def green_color(msg: str) -> str:
  return '\033[92m'+ msg + '\033[0m'


def checkargtypes(fn):
  sign = signature(fn)
  def wrapper_fn(**kwargs):
    def __check(param, arg_type, expected_type):
      if not issubclass(arg_type, expected_type):
        bf = build_file()
        loc = f'{fn.__name__} at {bf.filename}:{bf.lineno}'
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
