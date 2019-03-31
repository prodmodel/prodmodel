from model.py_file import PyFile


class PyFileCache:
  def __init__(self):
    self.cache = {}

  def get(self, file: str):
    if file not in self.cache:
      self.cache[file] = PyFile(file)
    return self.cache[file]
