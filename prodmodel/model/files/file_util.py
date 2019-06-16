import shutil
import os
from pathlib import Path

from prodmodel.globals import TargetConfig


def s3_local_file_name(s3_path) -> str:
    return TargetConfig.target_base_dir / 's3' / s3_path[5:] / 'cache'


def dest_dir(input_file) -> Path:
  d = TargetConfig.target_base_dir / 'data' / input_file.relative_name
  d.mkdir(parents=True, exist_ok=True)
  return d


def create_dest_file(args, input_file) -> Path:
  dest_path = dest_dir(input_file) / input_file.cached_hash_id
  if args.cache_data:
    if dest_path.is_symlink():
      os.remove(dest_path)
    if not dest_path.is_file():
      shutil.copy(input_file.file_name, dest_path)
  else:
    if not dest_path.is_file(): # Works with symlinks too.
      os.symlink(input_file.file_name, dest_path)
  return dest_path
