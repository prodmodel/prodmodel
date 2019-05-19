from pathlib import Path
import configparser


class TargetConfig:
  target_base_dir: Path


config = configparser.ConfigParser()

def load_config(path):
  config.read(config_file)
  
