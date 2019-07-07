import pickle
import json

from prodmodel.util import OUTPUT_FORMAT_TYPES


def save_output(file_path, output, output_format):
  assert output_format in OUTPUT_FORMAT_TYPES
  if output_format == 'pickle':
    with open(file_path, 'wb') as f:
      pickle.dump(output, f)
  else:
    with open(file_path, 'w') as f:
      json.dump(output, f)


def load_output(file_path, output_format):
  assert output_format in OUTPUT_FORMAT_TYPES
  if output_format == 'pickle':
    with open(file_path, 'rb') as f:
      return pickle.load(f)
  else:
    with open(file_path, 'r') as f:
      return json.load(f)


def output_file_name(output_format):
  assert output_format in OUTPUT_FORMAT_TYPES
  if output_format == 'pickle':
    return 'output_1.pickle'
  else:
    return 'output_1.json'
