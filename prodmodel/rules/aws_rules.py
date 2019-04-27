from typing import Tuple, List, Dict

from model.target.target import Target
from model.target.data_target import DataTarget
from model.target.s3_data_target import S3DataTarget
from util import checkargtypes


@checkargtypes
def copy_to_s3(data: Target, s3_bucket: str, s3_key: str) -> S3DataTarget:
  return S3DataTarget(data, s3_bucket, s3_key)
