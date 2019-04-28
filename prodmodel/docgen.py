#!/usr/bin/env python3.6

import os
import sys
import re
from inspect import getmembers, isfunction, signature


def gen_doc(module, f):
  for member in [member for member in getmembers(module) if isfunction(member[1])]:
    if member[1].__name__ == 'wrapper_fn':
      name = member[0]
      fn = member[1].__closure__[0].cell_contents
      sig_str = str(signature(fn))
      param_names = [p for p in signature(fn).parameters]
      for m in re.finditer('\`(\w)+\`', str(fn.__doc__)):
        param = str(m.group(0))[1:-1]
        assert param in param_names, f'{param} not in {param_names}'
      f.write(f'## {name}\n')
      f.write(f'`{name}{sig_str}`\n')
      if fn.__doc__:
        doc_str = re.sub('(\s)+', ' ', str(fn.__doc__)) 
        f.write(f'{doc_str}\n')
      f.write('\n')


if __name__ == "__main__":
  output = sys.argv[1]
  from rules import rules, aws_rules
  with open(output, 'w') as f:
    f.write('# Build rules\n\n')
    gen_doc(rules, f)
    gen_doc(aws_rules, f)
