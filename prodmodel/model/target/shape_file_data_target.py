from typing import List
import shapefile

from prodmodel.model.files.data_file import DataFile
from prodmodel.model.target.data_target import DataTarget


class ShapeFileDataTarget(DataTarget):
  def __init__(self, sources: List[DataFile]):
    super().__init__(sources=sources, deps=[], file_deps=[])
    self.sources = sources


  def execute(self):
    return shapefile.Reader(str(self.sources[0].file_name)).shapeRecords()
