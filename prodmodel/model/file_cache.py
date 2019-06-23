from prodmodel.model.files.py_file import PyFile


class PyFileCache:

  cache = {}

  @staticmethod
  def get(file: str) -> PyFile:
    if file not in PyFileCache.cache:
      PyFileCache.cache[file] = PyFile(file)
    return PyFileCache.cache[file]
