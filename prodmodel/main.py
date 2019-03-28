import sys
import rules
import importlib
import logging
import time
from os.path import abspath
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def main():
  # print command line arguments
  target_name = sys.argv[1:][0]

  start_time = time.time()
  root = Path(abspath('example'))
  spec = importlib.util.spec_from_file_location('build', root / 'build.py')
  mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  target = getattr(mod, target_name)
  target.init_with_deps()
  duration = round(time.time() - start_time, 3)
  logging.info(f'Init finished in {duration} secs.')
  result = target.output()
  end_time = time.time()
  duration = round(end_time - start_time, 3)
  logging.info(f'Build finished in {duration} secs.')
  logging.info(f'Created {result}.')


if __name__ == "__main__":
  main()
