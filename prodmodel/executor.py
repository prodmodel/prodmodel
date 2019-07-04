import argparse
import importlib
import logging
import os
import sys
import time
import pickle
from datetime import datetime
from pathlib import Path

from prodmodel.globals import TargetConfig, default_config, read_config
from prodmodel.model.target.target import Target
from prodmodel.model.files import file_util
from prodmodel.tools import cleaner


class ExecutorException(Exception):
  pass


BUILD = 'BUILD'
CLEAN = 'CLEAN'
LS    = 'LS'
HELP  = 'HELP'

__COMMANDS = [BUILD, CLEAN, LS, HELP]


def get_command():
  if len(sys.argv) > 1:
    command = sys.argv[1].upper()
    if command in __COMMANDS:
      return command
  return None


def _create_target_args(parser, with_command=True):
  if with_command:
    parser.add_argument('target', help='The target to execute in a <path_to_build_file>:<target> format, or ' +
                                       '<target> if the command is executed from the directory of the build file.')
  parser.add_argument('--target_dir', type=str, default='.target', help='The target directory to build in.')


__DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

def _parse_datetime(s: str):
  try:
    return datetime.strptime(s, __DATE_FORMAT)
  except Exception:
    raise ExecutorException(f'Datetime {s} has to be in {__DATE_FORMAT} format.')


__OUTPUT_FORMATS = ['none', 'str', 'bytes', 'log']

def _parse_output_format(s: str):
  if s not in __OUTPUT_FORMATS:
    output_formats = ', '.join(__OUTPUT_FORMATS)
    raise ExecutorException(f'Flag --output_type has to be one of {output_formats}.')
  return s


def _create_output_format_args(parser):
  parser.add_argument('--output_format', type=_parse_output_format, default='log',
    help='One of `none`, `str`, `bytes` and `log`. The output format of the data ' +
         'produced by the build target written to stdout.')


def create_arg_parser(command):
  parser = argparse.ArgumentParser(description='Build, deploy and test Python data science models.')
  if command is not None:
    parser.add_argument('command', help='The command to execute.')
  if command is None or command == BUILD:
    _create_target_args(parser)
    parser.add_argument('--force_external', action='store_true',
      help='Force reloading external data sources instead of using the cached data.')
    parser.add_argument('--cache_data', action='store_true',
      help='Cache local data files.')
    _create_output_format_args(parser)
    parser.add_argument('--build_time', type=int, default=int(time.time()))
  elif command == CLEAN:
    _create_target_args(parser)
    parser.add_argument(
      '--cutoff_date',
      type=_parse_datetime,
      default=datetime.now(),
      help=f'Clean up files modified before this datetime ({__DATE_FORMAT}), default now.')
  elif command == LS:
    parser.add_argument('build_file', type=str, help='The build file or the directory of the build file to list.')
    _create_target_args(parser, with_command=False)
    _create_output_format_args(parser)
  elif command == HELP:
    pass
  else:
    raise ExecutorException(f'Unknown command {command}.')
  return parser


def _resolve_build_file(f):
  if f.endswith('build.py'):
    return Path(f).resolve()
  else:
    return (Path(f) / 'build.py').resolve()


def _parse_target(target_arg):
  if ':' in target_arg:
    target_parts = target_arg.split(':')
    f = target_parts[0]
    target = target_parts[1]
    return _resolve_build_file(f), target
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
    read_config(config_file)

  rootLogger = logging.getLogger()
  rootLogger.setLevel(logging.DEBUG)

  fileHandler = logging.FileHandler(home_path / 'app.log')
  fileHandler.setLevel(default_config('FILE_LOG_LEVEL', logging.DEBUG))
  fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
  rootLogger.addHandler(fileHandler)

  consoleHandler = logging.StreamHandler()
  consoleHandler.setLevel(default_config('CONSOLE_LOG_LEVEL', logging.INFO))
  rootLogger.addHandler(consoleHandler)


def _set_s3_target_dir(build_file):
  s3_target_dir = default_config('S3_TARGET_DIR')
  if s3_target_dir:
    if not default_config('AWS_ACCESS_KEY_ID') or not default_config('AWS_SECRET_ACCESS_KEY'):
      raise ExecutorException('Cannot use S3_TARGET_DIR without AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.')
    pfx = s3_target_dir if s3_target_dir.endswith('/') else s3_target_dir + '/'
    sfx = '/'.join(build_file.relative_to(build_file.anchor).parts[:-1])
    s3_path = pfx + sfx
    TargetConfig.target_base_dir_s3_bucket = file_util.s3_bucket(s3_path)
    TargetConfig.target_base_dir_s3_key = file_util.s3_key(s3_path)


def process_target(args, fn, command_name):
  build_file, target_name = _parse_target(args.target)
  _setup_target_dirs(build_file, args.target_dir)

  logging.info(f'{command_name} target {target_name} in {build_file}.')
  build_mod = _load_build_mod(build_file)

  if target_name == '*':
    targets = []
    for target_name in dir(build_mod):
      target = getattr(build_mod, target_name)
      if isinstance(target, Target):
        targets.append((target_name, target))
  else:
    if target_name in dir(build_mod):
      target = getattr(build_mod, target_name)
      if isinstance(target, Target):
        targets = [(target_name, target)]
      else:
        raise ExecutorException(f'Variable "{target_name}" is not a target but a "{type(target).__name__}".')
    else:
      raise ExecutorException(f'Target "{target_name}" not found in {build_mod.__file__}.')
  for target_name, target in targets:
    fn(target=target, target_name=target_name, args=args)


def _output(args, result):
  if args.output_format == 'str':
    os.write(1, str(result).encode('utf-8'))
    logging.info('')
  elif args.output_format == 'bytes':
    os.write(1, pickle.dumps(result))
    logging.info('')
  elif args.output_format == 'log':
    logging.info(f'Created {result}.')


def list_commands():
  commands = ', '.join([command.lower() for command in __COMMANDS])
  logging.info(f'Supported commands: {commands}.')


def _setup_target_dirs(build_file, target_dir):
  if not build_file.is_file():
    raise ExecutorException(f'Build file {build_file} does not exist or not a file.')
  TargetConfig.target_base_dir = _target_dir(target_dir, build_file)
  _set_s3_target_dir(build_file)


def list_targets(args):
  build_file = _resolve_build_file(args.build_file)
  _setup_target_dirs(build_file, args.target_dir)

  targets = []
  build_mod = _load_build_mod(build_file)
  for target_name in dir(build_mod):
    target = getattr(build_mod, target_name)
    if isinstance(target, Target):
      targets.append(target_name)
  _output(args, targets)


def clean_target(target, args, **kwargs):
  cleaner.remove_old_cache_files(target, args.cutoff_date)


def build_target(target, args, target_name, **kwargs):
  logging.info(f'Initializing target {target_name}.')
  target.init_with_deps(args)
  logging.info(f'Target {target_name} initialized.')
  result = target.output()
  _output(args, result)
