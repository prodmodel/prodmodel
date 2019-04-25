#!/usr/bin/env python3.6

import sys
import importlib
import logging
import time
from os.path import abspath
from pathlib import Path
import os
import subprocess
import argparse

if __package__ == 'prodmodel':
  # To be able to import when run as an executable:
  path = os.path.dirname(__file__)
  sys.path.append(path)

from rules import rules
from model.target import Target
from util import red_color, green_color
from globals import TargetConfig


logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Build, deploy and test Python data science models.')
parser.add_argument('target', help='The target to execute in a <path_to_build_file>:<target> format, or <target> if the command is executed from the directory of the build file.')
parser.add_argument('--force_external', action='store_true', help='Force reloading external data sources instead of using the cached data.')
parser.add_argument('--cache_data', action='store_true', help='Cache local data files.')
parser.add_argument('--target_dir', type=str, default='.target', help='The target directory to build in.')
parser.add_argument('--build_time', type=int, default=int(time.time()))


def _parse_target(target_arg):
  if ':' in target_arg:
    target_parts = target_arg.split(':')
    f = target_parts[0]
    target = target_parts[1]
    if f.endswith('build.py'):
      return Path(f).resolve(), target
    else:
      return (Path(f) / 'build.py').resolve(), target
  else:
    return Path('build.py').resolve(), target_arg


def _load_build_mod(build_file):
  spec = importlib.util.spec_from_file_location('build', build_file)
  build_mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(build_mod)

  for field_name in dir(build_mod):
    field_obj = getattr(build_mod, field_name)
    if isinstance(field_obj, Target):
      field_obj.set_name(field_name)

  return build_mod


def _target_dir(args, build_file) -> Path:
  target_dir = Path(args.target_dir)
  if target_dir.is_absolute():
    return target_dir
  else:
    return build_file.parent / target_dir


def main():
  args = parser.parse_args()
  start_time = time.time()
  try:
    build_file, target_name = _parse_target(args.target)
    TargetConfig.target_base_dir = _target_dir(args, build_file)
    logging.info(f'Executing target {target_name} in {build_file}.')
    build_mod = _load_build_mod(build_file)
    if target_name in dir(build_mod):
      target = getattr(build_mod, target_name)
      if isinstance(target, Target):
        target.init_with_deps(args)
        result = target.output()
        logging.info(f'Created {result}.')
        success = True
      else:
        raise rules.RuleException(f'Variable "{target_name}" is not a target but a "{type(target).__name__}".')
    else:
      raise rules.RuleException(f'Target "{target_name}" not found in {build_mod.__file__}.')
  except rules.RuleException as e:
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
