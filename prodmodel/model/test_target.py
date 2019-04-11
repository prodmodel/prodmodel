from typing import List

from util import RuleException
from model.target import Target
from model.artifact import Artifact

import pytest


class TestTarget(Target):
  def __init__(self, test_file: Artifact, file_deps: List[Artifact], cache: bool):
    super().__init__(sources=[test_file], file_deps=file_deps, deps=[], cache=cache)
    self.test_file = test_file


  def execute(self):
    return_value = pytest.main([str(self.test_file.file_name)])
    if return_value > 0:
      raise RuleException('Test failed.')
    return 'Test result: OK'
