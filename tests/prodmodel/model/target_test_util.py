import os
import unittest
from pathlib import Path

from prodmodel import executor
from prodmodel.model.files.data_file import DataFile
from prodmodel.globals import TargetConfig


class TargetTestUtil(unittest.TestCase):

  @classmethod
  def setUp(self):
    root = Path(os.getcwd())
    TargetConfig.target_base_dir = root / '.target'
    args = executor.create_arg_parser().parse_args()
    self.data_file = DataFile(root / 'tests' / 'prodmodel' / 'data' / 'test.json')
    self.data_file.init(args)
