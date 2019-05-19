from pathlib import Path

from prodmodel.model.files.input_file import InputFile
from prodmodel.model.target.external_data_target import ExternalDataTarget


class ExternalDataFile(InputFile):

  def __init__(self, external_data_target: ExternalDataTarget):
    super().__init__(file_name=external_data_target.output_path().absolute())
    self.external_data_target = external_data_target
    self.cached_build_time = None


  def init_impl(self, args) -> Path:
    self.external_data_target.init_with_deps(args)
    path = Path(self.file_name)
    if args.force_external or not path.is_file():
      # Re-create input file.
      self.external_data_target.output(force=True)
    return path
