import os
import sys
from pathlib import Path
import logging
import importlib
import argparse
import time
from datetime import datetime

from prodmodel.rules import rules
from prodmodel.model.target.target import Target
from prodmodel.globals import TargetConfig, config
from prodmodel.util import red_color
from prodmodel.tools import cleaner


BUILD = 'BUILD'
CLEAN = 'CLEAN'

def get_command():
  if len(sys.argv) > 1:
    if sys.argv[1].upper() == CLEAN:
      return CLEAN
    elif sys.argv[1].upper() == BUILD:
      return BUILD
  return None


def _create_target_args(parser):
  parser.add_argument('target', help='The target to execute in a <path_to_build_file>:<target> format, or <target> if the command is executed from the directory of the build file.')
  parser.add_argument('--target_dir', type=str, default='.target', help='The target directory to build in.')


__DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

def _parse_datetime(s: str):
  try:
    return datetime.strptime(s, __DATE_FORMAT)
  except Exception as e:
    raise Exception(f'Datetime {s} has to be in {__DATE_FORMAT} format.')


def create_arg_parser(command):
  parser = argparse.ArgumentParser(description='Build, deploy and test Python data science models.')
  if command is None or command == BUILD:
    if command == BUILD:
      parser.add_argument('command', help='The command to execute.')
    _create_target_args(parser)
    parser.add_argument('--force_external', action='store_true', help='Force reloading external data sources instead of using the cached data.')
    parser.add_argument('--cache_data', action='store_true', help='Cache local data files.')
    parser.add_argument('--build_time', type=int, default=int(time.time()))
  elif command == CLEAN:
    parser.add_argument('command', help='The command to execute.')
    _create_target_args(parser)
    parser.add_argument(
      '--cutoff_date',
      type=_parse_datetime,
      default=datetime.now(),
      help=f'Clean up files modified before this datetime ({__DATE_FORMAT}), default now.')
  else:
    raise rules.RuleException(f'Unknown command {command}.')
  return parser


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


def _target_dir(args_target_dir, build_file) -> Path:
  target_dir = Path(args_target_dir)
  if target_dir.is_absolute():
    return target_dir
  else:
    return build_file.parent / target_dir


def setup():
  home_path = Path(os.path.expanduser('~')) / '.prodmodel'
  os.makedirs(home_path, exist_ok=True)

  config_file = home_path / 'config'
  if os.path.isfile(config_file):
    config.read(config_file)

  rootLogger = logging.getLogger()
  rootLogger.setLevel(logging.DEBUG)

  fileHandler = logging.FileHandler(home_path / 'app.log')
  fileHandler.setLevel(config['DEFAULT'].get('FILE_LOG_LEVEL', logging.DEBUG))
  fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
  rootLogger.addHandler(fileHandler)

  consoleHandler = logging.StreamHandler()
  consoleHandler.setLevel(config['DEFAULT'].get('CONSOLE_LOG_LEVEL', logging.INFO))
  rootLogger.addHandler(consoleHandler)


def process_target(args, fn, command_name):
  try:
    build_file, target_name = _parse_target(args.target)
    if not build_file.is_file():
      raise rules.RuleException(f'Build file {build_file} does not exist or not a file.')
    TargetConfig.target_base_dir = _target_dir(args.target_dir, build_file)
    logging.info(f'{command_name} target {target_name} in {build_file}.')
    build_mod = _load_build_mod(build_file)
    if target_name in dir(build_mod):
      target = getattr(build_mod, target_name)
      if isinstance(target, Target):
        fn(target=target, target_name=target_name, args=args)
        success = True
      else:
        raise rules.RuleException(f'Variable "{target_name}" is not a target but a "{type(target).__name__}".')
    else:
      raise rules.RuleException(f'Target "{target_name}" not found in {build_mod.__file__}.')
  except rules.RuleException as e:
    logging.error(red_color(str(e)))
    success = False
  return success


def clean_target(target, args, **kwargs):
  cleaner.remove_old_cache_files(target, args.cutoff_date)


def build_target(target, args, target_name, **kwargs):
  logging.info(f'Initializing target {target_name}.')
  target.init_with_deps(args)
  logging.info(f'Target {target_name} initialized.')
  result = target.output()
  logging.info(f'Created {result}.')
