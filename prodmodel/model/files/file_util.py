import shutil
import os

from globals import TargetConfig


def build_file(args, input_file):
  path = TargetConfig.target_base_dir / 'data' / input_file.relative_name / input_file.cached_hash_id
  path.parent.mkdir(parents=True, exist_ok=True)
  if args.cache_data:
    if path.is_symlink():
      os.remove(path)
    if not path.is_file():
      shutil.copy(input_file.file_name, path)
  else:
    if not path.is_file(): # Works with symlinks too.
      os.symlink(input_file.file_name, path)
  return path
