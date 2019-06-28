import boto3
import configparser
import os
from pathlib import Path


config = configparser.ConfigParser()


def default_config(name):
  return config['DEFAULT'].get(name, os.environ[name])


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
