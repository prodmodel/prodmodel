import hashlib
import json
import logging
import os
import shutil
import sys
from abc import abstractmethod
from pathlib import Path
from typing import List

from prodmodel import util
from prodmodel.globals import TargetConfig
from prodmodel.model.files.input_file import InputFile
from prodmodel.model.target import target_serializer


class Target:
  # TODO List[Target]
  def __init__(self, sources: List[InputFile], deps: List, file_deps: List[InputFile]=[]):
    self.sources = sources
    self.deps = deps
    self.cached_output = None
    self.cached_hash_id = None
    try:
      self.lineno = str(util.build_file().lineno)
    except Exception as e:
      logging.warning(e)
      self.lineno = -1
    self.name = None
    self.file_deps = file_deps
    transitive_file_deps = set(file_deps)
    for dep in deps:
      transitive_file_deps.update(dep.transitive_file_deps)
    self.transitive_file_deps = transitive_file_deps
    self.output_format = 'pickle'


  @abstractmethod
  def execute(self) -> object:
    pass


  @abstractmethod
  def params(self) -> dict:
    pass


  def init_with_deps(self, args):
    for source in self.sources:
      source.init(args)
    for file_dep in self.file_deps:
      file_dep.init(args)
    for dep in self.deps:
      dep.init_with_deps(args)



  def hash_id(self) -> str:
    m = hashlib.sha256()
    m.update(util.lib_hash_id().encode('utf-8'))
    m.update(self.__class__.__name__.encode('utf-8'))
    m.update(self.output_format.encode('utf-8'))
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


  def output_root_dir(self) -> Path:
    return TargetConfig.target_base_dir / 'output' / self._name()


  def _output_dir(self, hash_id) -> Path:
    return self.output_root_dir() / hash_id


  def output_dir(self) -> Path:
    return self._output_dir(self.hash_id())


  def output_path(self) -> Path:
    return self.output_dir() / target_serializer.output_file_name(self.output_format)


  def _get_metadata_from_dep(self, target, files, targets):
    def _rel_path(input_file):
      return str(input_file.dest_file_path.relative_to(TargetConfig.target_base_dir))

    for source in target.sources:
      files[_rel_path(source)] = source.hash_id()
    for file_dep in target.file_deps:
      files[_rel_path(file_dep)] = file_dep.hash_id()
    for dep in target.deps:
      dep_hash_id = dep.hash_id()
      if dep_hash_id not in targets:
        targets[str(dep._name())] = dep_hash_id
        self._get_metadata_from_dep(dep, files, targets)


  def _save_metadata(self, hash_id):
    files = {}
    targets = {}
    self._get_metadata_from_dep(self, files, targets)

    with open(self._output_dir(hash_id) / 'metadata.json', 'w') as f:
      json.dump({'files': files, 'targets': targets}, f)


  def _s3_path(self, file_path):
    rel_path = '/'.join(file_path.relative_to(TargetConfig.target_base_dir).parts)
    s3_bucket = str(TargetConfig.target_base_dir_s3_bucket)
    s3_key = str(TargetConfig.target_base_dir_s3_key + '/' + rel_path)
    return s3_bucket, s3_key


  def _create_output(self, file_path, hash_id):
    logging.debug(f'  Creating version {hash_id}.')
    lib_dir, mod_names = self._setup_modules()
    with util.IsolatedSysPath(mod_names):
      sys.path.append(str(lib_dir))
      output = self.execute()
      self._save_metadata(hash_id)
    target_serializer.save_output(file_path, output, self.output_format)
    if TargetConfig.target_base_dir_s3_bucket is not None:
      s3_bucket, s3_key = self._s3_path(file_path)
      logging.debug(f'  Uploading output to s3://{s3_bucket}/{s3_key}.')
      TargetConfig._s3().upload_file(str(file_path), s3_bucket, s3_key)
    return output


  def _download_output_from_s3(self, file_path):
    s3_bucket, s3_key = self._s3_path(file_path)
    response = TargetConfig._s3().get_object(Bucket=s3_bucket, Key=s3_key)
    logging.debug(f'  Downloading cached version from s3://{s3_bucket}/{s3_key}.')
    with open(file_path, 'wb') as f:
      f.write(response['Body'].read())


  def output(self, force=False):
    target_name = self._name()
    logging.debug(f'Executing {target_name} defined at build.py:{self.lineno}.')
    hash_id = self.hash_id()
    if hash_id == self.cached_hash_id and self.cached_output is not None:
      logging.debug(f'  Re-using cached version {hash_id}.')
      return self.cached_output
    else:
      root_dir = self._output_dir(hash_id)
      os.makedirs(root_dir, exist_ok=True)
      file_path = root_dir / target_serializer.output_file_name(self.output_format)
      if force:
        output = self._create_output(file_path, hash_id)
      else:
        if file_path.is_file():
          logging.debug(f'  Loading cached version {hash_id}.')
          output = target_serializer.load_output(file_path, self.output_format)
        elif TargetConfig.target_base_dir_s3_bucket is not None:
          try:
            self._download_output_from_s3(file_path)
            output = target_serializer.load_output(file_path, self.output_format)
          except Exception:
            output = self._create_output(file_path, hash_id)
        else:
          output = self._create_output(file_path, hash_id)
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
