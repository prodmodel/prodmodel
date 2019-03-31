import sys
import rules
import importlib
import logging
import time
from os.path import abspath
from pathlib import Path
import os
import subprocess
from rules import RuleException
from model.target import Target
from util import red_color, green_color


logging.basicConfig(level=logging.INFO)

def main():
  target_name = sys.argv[1:][0]

  sys.path = [path for path in sys.path if 'site-packages' not in path]

  start_time = time.time()
  root = Path(abspath('example'))
  build_file = root / 'build.py'
  spec = importlib.util.spec_from_file_location('build', build_file)
  build_mod = importlib.util.module_from_spec(spec)

  try:
    spec.loader.exec_module(build_mod)
    if target_name in dir(build_mod):
      target = getattr(build_mod, target_name)
      if isinstance(target, Target):
        target.init_with_deps()
        result = target.output()
        logging.info(f'Created {result}.')
        success = True
      else:
        raise RuleException(f'Variable "{target_name}" is not a target but a "{type(target).__name__}".')
    else:
      raise RuleException(f'Target "{target_name}" not found in {build_file}.')
  except RuleException as e:
    logging.error(red_color(str(e)))
    success = False

  end_time = time.time()
  duration = round(end_time - start_time, 3)
  if success:
    logging.info(green_color(f'Build successfully finished in {duration} secs.'))
    return 0
  else:
    logging.error(red_color(f'Build failed in {duration} secs.'))
    return 1


if __name__ == "__main__":
  main()
