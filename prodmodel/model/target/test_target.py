from typing import List

import pytest

from prodmodel.model.files.input_file import InputFile
from prodmodel.model.target.target import Target
from prodmodel.util import RuleException


class TestTarget(Target):
  def __init__(self, test_file: InputFile, file_deps: List[InputFile]):
    super().__init__(sources=[test_file], file_deps=file_deps, deps=[])
    self.test_file = test_file


  def execute(self):
    return_value = pytest.main([str(self.test_file.file_name)])
    if return_value > 0:
      raise RuleException('Test failed.')
    return 'Test result: OK'
