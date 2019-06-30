import boto3
import configparser
import os
from pathlib import Path


__config = configparser.ConfigParser()


def read_config(config_file):
  __config.read(config_file)


def default_config(name, default=None):
  return __config['DEFAULT'].get(name, os.environ.get(name, default))


class TargetConfig:
  target_base_dir: Path
  lib_dir: Path = None
  target_base_dir_s3_bucket: str = None
  target_base_dir_s3_key_prefix: str = None
  s3 = None

  @staticmethod
  def _s3():
    if TargetConfig.s3 is None:
      TargetConfig.s3 = boto3.client(
        's3',
        aws_access_key_id=default_config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=default_config('AWS_SECRET_ACCESS_KEY')
      )
    return TargetConfig.s3
