import sys
import rules
import importlib
import logging
import time
from os.path import abspath
from pathlib import Path
import os
import subprocess
import pip._internal

logging.basicConfig(level=logging.INFO)

def main():
  target_name = sys.argv[1:][0]

  lib_dir = str((Path('target') / 'lib').resolve())
  pip._internal.main(['install', f'--target={lib_dir}', '--ignore-installed', 'sklearn'])
  sys.path = [path for path in sys.path if 'site-packages' not in path]
  sys.path.insert(0, lib_dir)

  start_time = time.time()
  root = Path(abspath('example'))
  spec = importlib.util.spec_from_file_location('build', root / 'build.py')
  mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  target = getattr(mod, target_name)
  target.init_with_deps()

  result = target.output()
  end_time = time.time()
  duration = round(end_time - start_time, 3)
  logging.info(f'Build finished in {duration} secs.')
  logging.info(f'Created {result}.')


if __name__ == "__main__":
  main()
