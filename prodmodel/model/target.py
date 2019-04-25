from abc import abstractmethod
import hashlib
import pickle
from pathlib import Path
from os.path import abspath
import os
import logging
import json
import util
import sys
import shutil

from typing import List
from model.input_file import InputFile
from globals import TargetConfig


OUTPUT_FILE_NAME = 'output_1.pickle'


class Target:
  # TODO List[Target]
  def __init__(self, sources: List[InputFile], deps: List, file_deps: List[InputFile]=[], cache: bool=False):
    self.sources = sources
    self.deps = deps
    self.cache = cache
    self.cached_output = None
    self.cached_hash_id = None
    self.lineno = str(util.build_file().lineno)
    self.name = None
    self.file_deps = file_deps
    transitive_file_deps = set(file_deps)
    for dep in deps:
      transitive_file_deps.update(dep.transitive_file_deps)
    self.transitive_file_deps = transitive_file_deps


  @abstractmethod
  def is_changed(self):
    pass


  @abstractmethod
  def init(self):
    pass


  @abstractmethod
  def execute(self) -> object:
    pass


  @abstractmethod
  def finish(self):
    pass


  @abstractmethod
  def params(self) -> dict:
    pass


  def init_with_deps(self, args):
    self.init()
    for source in self.sources:
      source.init(args)
    for file_dep in self.file_deps:
      file_dep.init(args)
    for dep in self.deps:
      dep.init_with_deps(args)


  def finish_with_deps(self):
    self.finish()
    for dep in self.deps:
      dep.finish_with_deps()


  def hash_id(self) -> str:
    m = hashlib.sha256()
    m.update(util.lib_hash_id().encode('utf-8'))
    m.update(self.__class__.__name__.encode('utf-8'))
    m.update(json.dumps(self.params()).encode('utf-8'))
    for source in self.sources:
      m.update(source.hash_id().encode('utf-8'))
    for file_dep in self.file_deps:
      m.update(file_dep.hash_id().encode('utf-8'))
    for dep in self.deps:
      m.update(dep.hash_id().encode('utf-8'))
    return m.hexdigest()


  def _name(self):
    return self.name if self.name is not None else self.__class__.__name__


  def set_name(self, name: str):
    self.name = name


  def _output_dir(self, hash_id) -> Path:
    return TargetConfig.target_base_dir / 'output' / self._name() / hash_id


  def output_dir(self) -> Path:
    return self._output_dir(self.hash_id())


  def output_path(self) -> Path:
    return self.output_dir() / OUTPUT_FILE_NAME


  def output(self, force=False):
    target_name = self._name()
    logging.info(f'Executing {target_name} defined at build.py:{self.lineno}.')
    hash_id = self.hash_id()
    if hash_id == self.cached_hash_id and self.cached_output is not None:
      logging.info(f'  Re-using cached version {hash_id}.')
      return self.cached_output
    else:
      root_dir = self._output_dir(hash_id)
      os.makedirs(root_dir, exist_ok=True)
      file_path = root_dir / OUTPUT_FILE_NAME
      if not force and file_path.is_file():
        logging.info(f'  Loading cached version {hash_id}.')
        with open(file_path, 'rb') as f:
          output = pickle.load(f)
      else:
        logging.info(f'  Creating version {hash_id}.')
        lib_dir, mod_names = self._setup_modules()
        with util.IsolatedSysPath(mod_names):
          sys.path.append(str(lib_dir))
          output = self.execute()
        with open(file_path, 'wb') as f:
          pickle.dump(output, f)
      self.cached_output = output
      self.cached_hash_id = hash_id
      return output


  def _setup_modules(self):
    lib_dir = self.output_dir() / 'lib'
    shutil.rmtree(lib_dir, ignore_errors=True)
    lib_dir.mkdir(parents=True, exist_ok=True)
    mod_names = []
    for f in self.transitive_file_deps:
      os.symlink(f.file_name, lib_dir / f.file_name.name)
      mod_names.append(f.mod_name())
    return lib_dir, mod_names
        
