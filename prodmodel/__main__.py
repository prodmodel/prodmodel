#!/usr/bin/env python3.6

import sys
import importlib
import logging
import time
import os
import subprocess

import prodmodel
from prodmodel import executor
from prodmodel.util import red_color, green_color


def main():
  command = executor.get_command()
  parser = executor.create_arg_parser(command)

  executor.setup()
  if hasattr(prodmodel, '__version__'):
    logging.debug(f'Running Prodmodel version {prodmodel.__version__}.')
  args = parser.parse_args()
  if command == executor.BUILD:
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
  elif command == executor.CLEAN:
    start_time = time.time()
    executor.clean_target(args)
    end_time = time.time()
    duration = round(end_time - start_time, 3)

    logging.info(green_color(f'Cleanup successfully finished in {duration} secs.'))
    return 0


if __name__ == "__main__":
  main()
