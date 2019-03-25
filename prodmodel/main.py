import sys
import rules
import importlib
import logging
from os.path import abspath
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def main():
  # print command line arguments
  target = sys.argv[1:][0]

  root = Path(abspath('example'))
  spec = importlib.util.spec_from_file_location('build', root / 'build.py')
  mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  result = getattr(mod, target).output()
  logging.info(f'Created {result}.')



if __name__ == "__main__":
  main()
