from pathlib import Path
import configparser


class TargetConfig:
  target_base_dir: Path


_config = configparser.ConfigParser()


def load_config(path):
  _config.read(path)


def get_config():
  return _config
