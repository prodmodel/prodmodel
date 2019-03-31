from typing import List

from util import RuleException, IsolatedSysPath
from model.target import Target
from model.artifact import Artifact

import pytest
import sys
from pathlib import Path


class TestTarget(Target):
  def __init__(self, test_file: Artifact, source_files: List[Artifact], cache: bool):
    super().__init__(sources=[test_file] + source_files, deps=[], cache=cache)
    self.test_file = test_file
    self.source_files = source_files


  def execute(self):
    dirs = list(set([str(Path(f.file_name).parent) for f in self.source_files]))
    with IsolatedSysPath():
      sys.path.extend(dirs)
      return_value = pytest.main([str(self.test_file.file_name)])
    if return_value > 0:
      raise RuleException('Test failed.')
    return 'Test result: OK'
