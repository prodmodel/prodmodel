import importlib
import shutil
import os
from pathlib import Path
import boto3
import json
import datetime
import logging

from prodmodel.model.files.input_file import InputFile
from prodmodel.model.files.file_util import create_dest_file, dest_dir, s3_local_file_name


class S3DataFile(InputFile):

  def __init__(self, s3_path: str):
    assert s3_path.startswith('s3://')
    super().__init__(file_name=s3_local_file_name(s3_path))
    self.cached_build_time = None
    self.s3_path = s3_path
    self.s3_bucket = s3_path[5:s3_path.index('/', 5)]
    self.s3_key = s3_path[s3_path.index('/', 5)  + 1:]
    self.s3 = None


  def _s3(self):
    if self.s3 is None:
      self.s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
      )
    return self.s3


  def init_impl(self, args) -> Path:
    metadata_file = self.file_name.parent / 'metadata.json'
    if metadata_file.is_file():
      with open(metadata_file, 'r') as f:
        metadata = json.load(f)
      local_last_modified = metadata['last_modified']
    else:
      local_last_modified = None

    response = self._s3().get_object(Bucket=self.s3_bucket, Key=self.s3_key)
    s3_last_modified = response['LastModified'].isoformat()
    if local_last_modified != s3_last_modified:
      self.file_name.parent.mkdir(parents=True, exist_ok=True)
      logging.debug(f'Downloading s3://{self.s3_bucket}/{self.s3_key} to {self.file_name}.')
      with open(self.file_name, 'wb') as f:
        f.write(response['Body'].read())
      with open(metadata_file, 'w') as f:
        json.dump({'last_modified': s3_last_modified}, f)
    else:
      logging.debug(f'Using cached version of s3://{self.s3_bucket}/{self.s3_key}: {self.file_name}.')

    self.cached_hash_id = self.hash_id()
    return create_dest_file(args, self)
