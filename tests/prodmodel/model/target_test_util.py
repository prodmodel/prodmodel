import os
import unittest
from pathlib import Path

from prodmodel import executor
from prodmodel.model.files.data_file import DataFile
from prodmodel.globals import TargetConfig


class TargetTestUtil(unittest.TestCase):

  @classmethod
  def setUp(self):
    TargetConfig.target_base_dir = Path(os.getcwd())
    args = executor.create_arg_parser().parse_args()
    self.data_file = DataFile(TargetConfig.target_base_dir / 'tests' / 'prodmodel' / 'data' / 'test.json')
    self.data_file.init(args)
