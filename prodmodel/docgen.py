#!/usr/bin/env python3.6

import re
import sys
from inspect import Signature, getmembers, isfunction, signature
from typing import GenericMeta

from prodmodel.rules.rules import EXTRA_DOC_PARAMS


def _annotation_str(a):
  if isinstance(a, GenericMeta) and a.__extra__ == dict and a.__args__:
    return f'{a.__name__}[{a.__args__[0].__name__}, {a.__args__[1].__name__}]'
  elif isinstance(a, GenericMeta) and a.__extra__ == list and a.__args__:
    return f'{a.__name__}[{a.__args__[0].__name__}]'
  elif isinstance(a, GenericMeta) and a.__extra__ == tuple and a.__args__:
    args_str = ', '.join([arg.__name__ for arg in a.__args__])
    return f'{a.__name__}[{args_str}]'
  else:
    return f'{a.__name__}'


def gen_doc(module, f):
  for member in [member for member in getmembers(module) if isfunction(member[1])]:
    if member[1].__name__ == 'wrapper_fn':
      name = member[0]
      fn = member[1].__closure__[0].cell_contents
      p_strs = []
      sign = signature(fn)
      for p in sign.parameters:
        a = sign.parameters[p].annotation
        p_strs.append(f'{p}: {_annotation_str(a)}')
      if sign.return_annotation == Signature.empty:
        ret_str = ''
      else:
        ret_str = ' -> ' + _annotation_str(sign.return_annotation)
      sig_str = f'''{name}({', '.join(p_strs)}){ret_str}'''

      param_names = [p for p in sign.parameters]
      params_in_doc = set()
      for m in re.finditer('\`(\w)+\`', str(fn.__doc__)):
        params_in_doc.add(str(m.group(0))[1:-1])

      for param in params_in_doc:
        assert param in param_names, f'Param {param} is not in the signature of {name} ({param_names}).'
      for param in param_names:
        assert param in params_in_doc or param in EXTRA_DOC_PARAMS, f'Param {param} of {name} is undocumented ({params_in_doc}).'

      f.write(f'## {name}\n\n')
      f.write(f'`{sig_str}`<br/>\n\n')
      if fn.__doc__:
        doc_str = re.sub('(\s)+', ' ', str(fn.__doc__)).replace('<br>', '<br>\n')
        f.write(f'{doc_str}<br>\n\n')
        for param in param_names:
          if param not in params_in_doc:
            extra_doc_str = re.sub('(\s)+', ' ', EXTRA_DOC_PARAMS[param]).replace('<br>', '<br>\n')
            f.write(extra_doc_str + '<br>\n\n')
      f.write('\n')


if __name__ == "__main__":
  output = sys.argv[1]
  from prodmodel.rules import rules, aws_rules
  with open(output, 'w') as f:
    f.write('# Build rules\n\n')
    gen_doc(rules, f)
    gen_doc(aws_rules, f)
