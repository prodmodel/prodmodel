import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from prodmodel.model.target.target import Target


def remove_old_cache_files(target: Target, cutoff_date: datetime):
  deleted_cnt = 0
  root_dir = target.output_root_dir()
  if root_dir.is_dir():
    for d in target.output_root_dir().iterdir():
      if d.is_dir():
        metadata_file = Path(d / 'metadata.json')
        if metadata_file.is_file():
          last_modified_datetime = datetime.fromtimestamp(os.path.getmtime(metadata_file))
          if last_modified_datetime < cutoff_date:
            logging.debug('Deleting cache dir {d}.'.format(d=d))
            shutil.rmtree(d)
            deleted_cnt = deleted_cnt + 1
  else:
    logging.warning('Target output root dir {root_dir} does not exist.'.format(root_dir=root_dir))
  logging.info('Deleted {deleted_cnt} cached target outputs of target {target_name}.'.format(
    deleted_cnt=deleted_cnt, target_name=target.name))
