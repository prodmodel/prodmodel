from pathlib import Path
import os
import shutil
import logging
from datetime import datetime

from prodmodel.model.target.target import Target


def remove_old_cache_files(target: Target, cutoff_date: datetime):
  deleted_cnt = 0
  for d in target.output_root_dir().iterdir():
    if d.is_dir():
      metadata_file = Path(d / 'metadata.json')
      if metadata_file.is_file():
        last_modified_datetime = datetime.fromtimestamp(os.path.getmtime(metadata_file))
        if last_modified_datetime < cutoff_date:
          logging.debug(f'Deleting cache dir {d}.')
          shutil.rmtree(d)
          deleted_cnt = deleted_cnt + 1
  logging.info(f'Deleted {deleted_cnt} cached target outputs.')
