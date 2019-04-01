import boto3
import os


from model.target import Target
from model.data_target import DataTarget


class S3DataTarget(Target):
  def __init__(self, data: DataTarget, s3_bucket: str, s3_key: str):
    super().__init__(sources=[], deps=[data], cache=False)
    self.s3_key = s3_key
    self.s3_bucket = s3_bucket
    self.data = data
    self.s3 = boto3.client(
      's3',
      aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )


  def params(self) -> dict:
    return {'s3_bucket': self.s3_bucket, 's3_key': self.s3_key}


  def execute(self):
    self.data.output()
    path = self.data.output_path()
    self.s3.upload_file(path, self.s3_bucket, self.s3_key)
    return self.params()
