from model.py_file import PyFile


class PyFileCache:

  cache = {}

  def get(file: str):
    if file not in PyFileCache.cache:
      PyFileCache.cache[file] = PyFile(file)
    return PyFileCache.cache[file]
