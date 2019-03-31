from typing import Dict
from functools import partial

from model.artifact import Artifact
from model.data_target import DataTarget
from model.iterable_data_target import IterableDataTarget


class TransformStreamDataTarget(IterableDataTarget):
  def __init__(self, stream: IterableDataTarget, source: Artifact, objects: Dict[str, DataTarget], cache: bool):
    super().__init__(sources=[source], deps=[stream] + list(objects.values()), cache=cache)
    self.stream = stream
    self.source = source
    self.objects = objects


  def __iter__(self):
    mod = self.source.output()
    assert 'transform_record' in dir(mod)
    objects = {k: v.output() for k, v in self.objects.items()}
    map_fn = partial(mod.transform_record, **objects)
    return map(map_fn, self.stream.__iter__())
