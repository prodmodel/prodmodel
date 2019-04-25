from typing import Dict, List

from model.input_file import InputFile
from model.data_target import DataTarget
from model.iterable_data_target import IterableDataTarget


class TransformDataTarget(DataTarget):
  def __init__(self, source: InputFile, fn: str, streams: Dict[str, IterableDataTarget], objects: Dict[str, DataTarget], file_deps: List[InputFile], cache: bool):
    super().__init__(sources=[source], deps=list(streams.values()) + list(objects.values()), file_deps=file_deps, cache=cache)
    self.source = source
    self.streams = streams
    self.objects = objects
    self.fn = fn


  def execute(self):
    transform_fn = self.source.method(self.fn)
    streams = {k: v.__iter__() for k, v in self.streams.items()}
    objects = {k: v.output() for k, v in self.objects.items()}
    return transform_fn(**{**streams, **objects})
