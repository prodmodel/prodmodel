import shutil
import os

from prodmodel.globals import TargetConfig


def create_dest_file(args, input_file):
  dest_path = TargetConfig.target_base_dir / 'data' / input_file.relative_name / input_file.cached_hash_id
  dest_path.parent.mkdir(parents=True, exist_ok=True)
  if args.cache_data:
    if dest_path.is_symlink():
      os.remove(dest_path)
    if not dest_path.is_file():
      shutil.copy(input_file.file_name, dest_path)
  else:
    if not dest_path.is_file(): # Works with symlinks too.
      os.symlink(input_file.file_name, dest_path)
  return dest_path
