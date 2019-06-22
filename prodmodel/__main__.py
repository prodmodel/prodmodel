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
  executor.setup()

  command = executor.get_command()
  parser = executor.create_arg_parser(command)
  args = parser.parse_args()

  if hasattr(prodmodel, '__version__'):
    logging.debug(f'Running Prodmodel version {prodmodel.__version__}.')

  start_time = time.time()
  if command is None or command == executor.BUILD:
    command_name = 'Build'
    command_fn = executor.build_target
  elif command == executor.CLEAN:
    command_name = 'Cleaning'
    command_fn = executor.clean_target
  else:
    logging.error(red_color(f'Unknown command {command}.'))
    return 1

  success = executor.process_target(args, command_fn, command_name)
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
