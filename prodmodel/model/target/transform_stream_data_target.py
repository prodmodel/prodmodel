from functools import partial
from typing import Dict, List

from prodmodel.model.files.input_file import InputFile
from prodmodel.model.target.data_target import DataTarget
from prodmodel.model.target.iterable_data_target import IterableDataTarget


class TransformStreamDataTarget(IterableDataTarget):
  def __init__(self,
               source: InputFile,
               fn: str,
               stream: IterableDataTarget,
               objects: Dict[str, DataTarget],
               file_deps: List[InputFile],
               output_format: str):
    super().__init__(sources=[source], deps=[stream] + list(objects.values()), file_deps=file_deps, output_format=output_format)
    self.stream = stream
    self.source = source
    self.objects = objects
    self.fn = fn


  def __iter__(self):
    transform_record_fn = self.source.method(self.fn)
    objects = {k: v.output() for k, v in self.objects.items()}
    map_fn = partial(transform_record_fn, **objects)
    return map(map_fn, self.stream.__iter__())
