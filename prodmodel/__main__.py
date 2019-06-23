#!/usr/bin/env python3.6

import logging
import time

import prodmodel
from prodmodel import executor
from prodmodel.util import green_color, red_color, RuleException


def main():
  executor.setup()

  start_time = time.time()
  try:
    command = executor.get_command()
    parser = executor.create_arg_parser(command)
    args = parser.parse_args()

    # pylint: disable=E1101
    if hasattr(prodmodel, '__version__'):
      logging.debug(f'Running Prodmodel version {prodmodel.__version__}.')

    if command is None or command == executor.BUILD:
      command_name = 'Build'
      command_fn = executor.build_target
    elif command == executor.CLEAN:
      command_name = 'Cleaning'
      command_fn = executor.clean_target
    else:
      logging.error(red_color(f'Unknown command {command}.'))
      return 1

    executor.process_target(args, command_fn, command_name)
    success = True
  except (executor.ExecutorException, RuleException) as e:
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
