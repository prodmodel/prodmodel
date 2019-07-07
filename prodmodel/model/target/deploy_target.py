import shutil

from prodmodel.model.target.target import Target


class DeployTarget(Target):
  def __init__(self, data: Target, deploy_path: str):
    super().__init__(sources=[], deps=[data], file_deps=[])
    self.data = data
    self.deploy_path = deploy_path


  def params(self) -> dict:
    return {'deploy_path': self.deploy_path}


  def execute(self):
    self.data.output()
    source_path = str(self.data.output_path())
    shutil.copy(source_path, self.deploy_path)
    return self.params()
