import configparser
from pathlib import Path


class TargetConfig:
  target_base_dir: Path
  lib_dir: Path = None


config = configparser.ConfigParser()
