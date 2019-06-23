from pathlib import Path

from prodmodel.model.files.file_util import create_dest_file
from prodmodel.model.files.input_file import InputFile


class DataFile(InputFile):

  def __init__(self, file_name: str):
    super().__init__(file_name=file_name)
    self.cached_build_time = None


  def init_impl(self, args) -> Path:
    self.cached_hash_id = self.hash_id()
    return create_dest_file(args, self)
