from prodmodel import util
from prodmodel.model.target.target import Target


class S3DataTarget(Target):
  def __init__(self, data: Target, s3_bucket: str, s3_key: str):
    super().__init__(sources=[], deps=[data], file_deps=[])
    self.s3_key = s3_key
    self.s3_bucket = s3_bucket
    self.data = data
    self.s3 = None


  def _s3(self):
    if self.s3 is None:
      self.s3 = util.s3_client()
    return self.s3


  def params(self) -> dict:
    return {'s3_bucket': self.s3_bucket, 's3_key': self.s3_key}


  def execute(self):
    self.data.output()
    source_path = str(self.data.output_path())
    self._s3().upload_file(source_path, self.s3_bucket, self.s3_key)
    return self.params()
