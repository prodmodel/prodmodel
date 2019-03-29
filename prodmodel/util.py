import traceback

def build_file():
  for stack_frame in traceback.extract_stack():
    if stack_frame.filename.endswith('build.py'):
      return stack_frame
