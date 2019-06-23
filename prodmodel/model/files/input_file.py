import hashlib
import json
import logging
import os
from abc import abstractmethod
from datetime import datetime
from pathlib import Path

from prodmodel import util
from prodmodel.model.files.file_util import dest_dir

BLOCKSIZE = 65536


class InputFile:

  def __init__(self, file_name: str):
    if Path(file_name).is_absolute():
      self.file_name = Path(file_name)
      self.relative_name = Path(file_name).relative_to('/')
    else:
      root = Path(util.build_file().filename).parent
      self.file_name = root / file_name
      self.relative_name = Path(file_name)
    self.last_modified = None
    self.cached_hash_id = None
    self.cached_build_time = None


  def init(self, args):
    if self.cached_build_time != args.build_time:
      self.dest_file_path = self.init_impl(args)
      self.cached_build_time = args.build_time


  @abstractmethod
  def init_impl(self, args) -> Path:
    pass


  def _compute_hash(self):
    logging.debug(f'Computing hash id of {self.file_name}.')
    m = hashlib.md5()
    with open(self.file_name, 'rb') as f:
      buf = f.read(BLOCKSIZE)
      while len(buf) > 0:
        m.update(buf)
        buf = f.read(BLOCKSIZE)
    return m.hexdigest()


  def hash_id(self):
    last_modified = datetime.fromtimestamp(os.path.getmtime(self.file_name)).isoformat()

    if self.last_modified == last_modified and self.cached_hash_id:
      return self.cached_hash_id

    metadata_file = dest_dir(self) / 'metadata.json'
    if metadata_file.is_file():
      with open(metadata_file, 'r') as f:
        metadata = json.load(f)
      saved_last_modified = metadata['last_modified']
      if saved_last_modified == last_modified:
        logging.debug(f'Using locally cached hash id for {self.file_name}.')
        self.last_modified = last_modified
        self.cached_hash_id = metadata['hash_id']
        return self.cached_hash_id

    self.cached_hash_id = self._compute_hash()
    self.last_modified = last_modified
    with open(metadata_file, 'w') as f:
      json.dump({'last_modified': self.last_modified, 'hash_id': self.cached_hash_id}, f)

    return self.cached_hash_id
