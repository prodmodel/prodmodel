import os
import unittest
from pathlib import Path

from prodmodel import executor
from prodmodel.globals import TargetConfig
from prodmodel.model.files.data_file import DataFile
from prodmodel.model.files.py_file import PyFile


class TargetTestUtil(unittest.TestCase):

  @classmethod
  def setUp(self):
    root = Path(os.getcwd())
    TargetConfig.target_base_dir = root / '.target'
    args = executor.create_arg_parser(command=None).parse_args()

    self.json_data_file = DataFile(root / 'tests' / 'prodmodel' / 'data' / 'test.json')
    self.json_data_file.init(args)
    self.csv_data_file = DataFile(root / 'tests' / 'prodmodel' / 'data' / 'test.csv')
    self.csv_data_file.init(args)

    self.py_file = PyFile(str(root / 'tests' / 'prodmodel' / 'data' / 'test.py'))
    self.py_file.init(args)
