from model.files.py_file import PyFile


class PyFileCache:

  cache = {}

  def get(file: str) -> PyFile:
    if file not in PyFileCache.cache:
      PyFileCache.cache[file] = PyFile(file)
    return PyFileCache.cache[file]
