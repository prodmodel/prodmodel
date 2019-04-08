from model.artifact import Artifact
from model.external_data_target import ExternalDataTarget

from pathlib import Path


class ExternalDataArtifact(Artifact):

  def __init__(self, external_data_target: ExternalDataTarget):
    super().__init__(file_name=external_data_target.output_path().absolute())
    self.external_data_target = external_data_target
    self.cached_build_time = None


  def init(self, args):
    if (args.force_external and args.build_time != self.cached_build_time) or not Path(self.file_name).is_file():
      self.external_data_target.output(force=True)
      self.cached_build_time = args.build_time
