import os
from pathlib import Path
import logging
import importlib

from prodmodel.rules import rules
from prodmodel.model.target.target import Target
from prodmodel.globals import TargetConfig, config
from prodmodel.util import red_color


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


def run_target(args):
  try:
    build_file, target_name = _parse_target(args.target)
    TargetConfig.target_base_dir = _target_dir(args, build_file)
    logging.info(f'Executing target {target_name} in {build_file}.')
    build_mod = _load_build_mod(build_file)
    if target_name in dir(build_mod):
      target = getattr(build_mod, target_name)
      if isinstance(target, Target):
        logging.info(f'Initializing target {target_name}.')
        target.init_with_deps(args)
        logging.info(f'Target {target_name} initialized.')
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
  return success  
