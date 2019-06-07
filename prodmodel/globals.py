from pathlib import Path
import configparser


class TargetConfig:
  target_base_dir: Path
  lib_dir: Path = None


config = configparser.ConfigParser()
