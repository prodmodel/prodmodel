from typing import List

from util import RuleException, IsolatedSysPath
from model.target import Target
from model.artifact import Artifact

import pytest
import sys
from pathlib import Path
import shutil


class TestTarget(Target):
  def __init__(self, test_file: Artifact, source_files: List[Artifact], cache: bool):
    super().__init__(sources=[test_file] + source_files, deps=[], cache=cache)
    self.test_file = test_file
    self.source_files = source_files


  def execute(self):
    lib_dir = self.output_dir() / 'lib'
    lib_dir.mkdir(parents=True, exist_ok=True)
    for f in self.source_files:
      shutil.copy(f.file_name, lib_dir)
    with IsolatedSysPath():
      sys.path.append(str(lib_dir))
      return_value = pytest.main([str(self.test_file.file_name)])
    if return_value > 0:
      raise RuleException('Test failed.')
    return 'Test result: OK'
