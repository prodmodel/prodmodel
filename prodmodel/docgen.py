#!/usr/bin/env python3.6

import os
import sys
import re
from inspect import getmembers, isfunction, signature, Signature
from typing import List, Dict, GenericMeta


def gen_doc(module, f):
  for member in [member for member in getmembers(module) if isfunction(member[1])]:
    if member[1].__name__ == 'wrapper_fn':
      name = member[0]
      fn = member[1].__closure__[0].cell_contents
      p_strs = []
      sign = signature(fn)
      for p in sign.parameters:
        a = sign.parameters[p].annotation
        if isinstance(a, GenericMeta) and a.__extra__ == dict and a.__args__:
          p_strs.append(f'''{p}: {a.__name__}[{a.__args__[0].__name__}, {a.__args__[1].__name__}]''') 
        elif isinstance(a, GenericMeta) and a.__extra__ == list and a.__args__:
          p_strs.append(f'''{p}: {a.__name__}[{a.__args__[0].__name__}]''')
        else:
          p_strs.append(f'{p}: {a.__name__}')
      if sign.return_annotation == Signature.empty:
        ret_str = ''
      else:
        ret_str = ' -> ' + sign.return_annotation.__name__
      sig_str = f'''{name}({', '.join(p_strs)}){ret_str}'''

      param_names = [p for p in sign.parameters]
      for m in re.finditer('\`(\w)+\`', str(fn.__doc__)):
        param = str(m.group(0))[1:-1]
        assert param in param_names, f'{param} not in {param_names}'
      f.write(f'## {name}\n')
      f.write(f'`{name}{sig_str}`<br/>\n')
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
