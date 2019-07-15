from typing import Dict
import shapefile

from prodmodel.model.files.data_file import DataFile
from prodmodel.model.target.data_target import DataTarget


class ShapeFileDataTarget(DataTarget):
  def __init__(self, sources: Dict[str, DataFile]):
    super().__init__(sources=list(sources.values()), deps=[], file_deps=[])
    self.shape_files = sources


  def execute(self):
    return shapefile.Reader(str(self.shape_files['shp'].file_name)).shapeRecords()
