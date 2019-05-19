#!/usr/bin/env python3.6

import sys
import importlib
import logging
import time
import os
import subprocess
import argparse

import prodmodel
from prodmodel import executor
from prodmodel.util import red_color, green_color


def main():
  parser = argparse.ArgumentParser(description='Build, deploy and test Python data science models.')
  parser.add_argument('target', help='The target to execute in a <path_to_build_file>:<target> format, or <target> if the command is executed from the directory of the build file.')
  parser.add_argument('--force_external', action='store_true', help='Force reloading external data sources instead of using the cached data.')
  parser.add_argument('--cache_data', action='store_true', help='Cache local data files.')
  parser.add_argument('--target_dir', type=str, default='.target', help='The target directory to build in.')
  parser.add_argument('--build_time', type=int, default=int(time.time()))

  executor.setup()
  if hasattr(prodmodel, '__version__'):
    logging.debug(f'Running Prodmodel version {prodmodel.__version__}.')
  args = parser.parse_args()
  start_time = time.time()
  success = executor.run_target(args)
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
