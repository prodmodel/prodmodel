from pathlib import Path


SHAPE_FILE_EXTENSIONS = ['shp', 'shx', 'dbf', 'prj', 'xml', 'sbn', 'sbx', 'cpg']

def enumerate_shape_files(base_name: str):
  if '.' in base_name:
    if base_name[base_name.rfind('.') + 1:] in SHAPE_FILE_EXTENSIONS:
      resolved_name = base_name[:base_name.rfind('.')]
    else:
      resolved_name = base_name
  else:
    resolved_name = base_name
  return [resolved_name + '.' + ext for ext in SHAPE_FILE_EXTENSIONS]
