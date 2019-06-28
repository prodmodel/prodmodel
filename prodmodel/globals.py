import boto3
import configparser
import os
from pathlib import Path


config = configparser.ConfigParser()


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
        aws_access_key_id=config['DEFAULT'].get('AWS_ACCESS_KEY_ID', os.environ['AWS_ACCESS_KEY_ID']),
        aws_secret_access_key=config['DEFAULT'].get('AWS_SECRET_ACCESS_KEY', os.environ['AWS_SECRET_ACCESS_KEY'])
      )
    return TargetConfig.s3
