import traceback
import sys
from pathlib import Path


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
