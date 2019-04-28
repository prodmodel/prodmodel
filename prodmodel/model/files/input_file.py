from abc import abstractmethod
from datetime import datetime
import os
import hashlib
from pathlib import Path
import util


BLOCKSIZE = 65536


class InputFile:

  def __init__(self, file_name: str):
    if Path(file_name).is_absolute():
      self.file_name = Path(file_name)
    else:
      root = Path(util.build_file().filename).parent
      self.file_name = root / file_name
      self.relative_name = Path(file_name)
    self.last_modified = None
    self.cached_hash_id = None


  def init(self, args):
    if self.cached_build_time != args.build_time:
      self.dest_file_path = self.init_impl(args)
      self.cached_build_time = args.build_time


  @abstractmethod
  def init_impl(self, args) -> Path:
    pass


  def _compute_hash(self):
    m = hashlib.md5()
    with open(self.file_name, 'rb') as f:
      buf = f.read(BLOCKSIZE)
      while len(buf) > 0:
        m.update(buf)
        buf = f.read(BLOCKSIZE)
    return m.hexdigest()


  def hash_id(self):
    last_modified = os.path.getmtime(self.file_name)
    if self.last_modified == last_modified and self.cached_hash_id:
      return self.cached_hash_id

    self.cached_hash_id = self._compute_hash()
    self.last_modified = last_modified
    return self.cached_hash_id
