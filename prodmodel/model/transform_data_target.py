from typing import Dict

from model.artifact import Artifact
from model.data_target import DataTarget
from model.iterable_data_target import IterableDataTarget


class TransformDataTarget(DataTarget):
  def __init__(self, source: Artifact, streams: Dict[str, IterableDataTarget], objects: Dict[str, DataTarget], cache: bool):
    super().__init__(sources=[source], deps=list(streams.values()) + list(objects.values()), cache=cache)
    self.source = source
    self.streams = streams
    self.objects = objects


  def execute(self):
    mod = self.source.output()
    assert 'transform' in dir(mod)
    streams = {k: v.__iter__() for k, v in self.streams.items()}
    objects = {k: v.output() for k, v in self.objects.items()}
    return mod.transform(**{**streams, **objects})
