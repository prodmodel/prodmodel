#!/usr/bin/env python3

import re
import sys
from inspect import Signature, getmembers, isfunction, signature
from typing import GenericMeta

from prodmodel.rules.rules import EXTRA_DOC_PARAMS


def _annotation_str(a):
  if isinstance(a, GenericMeta) and a.__extra__ == dict and a.__args__:
    return '{t}[{a1}, {a2}]'.format(t=a.__name__, a1=a.__args__[0].__name__, a2=a.__args__[1].__name__)
  elif isinstance(a, GenericMeta) and a.__extra__ == list and a.__args__:
    return '{t}[{a}]'.format(t=a.__name__, a=a.__args__[0].__name__)
  elif isinstance(a, GenericMeta) and a.__extra__ == tuple and a.__args__:
    args_str = ', '.join([arg.__name__ for arg in a.__args__])
    return '{t}[{args_str}]'.format(t=a.__name__, args_str=args_str)
  elif a.__name__ == 'Tuple':
    args_str = ', '.join([arg.__name__ for arg in a.__tuple_params__])
    return '{t}[{args_str}]'.format(t=a.__name__, args_str=args_str)
  else:
    return '{t}'.format(t=a.__name__)


def gen_doc(module, f):
  for member in [member for member in getmembers(module) if isfunction(member[1])]:
    if member[1].__name__ == 'wrapper_fn':
      name = member[0]
      fn = member[1].__closure__[0].cell_contents
      p_strs = []
      sign = signature(fn)
      for p in sign.parameters:
        a = sign.parameters[p].annotation
        p_strs.append('{p}: {a}'.format(p=p, a=_annotation_str(a)))
      if sign.return_annotation == Signature.empty:
        ret_str = ''
      else:
        ret_str = ' -> ' + _annotation_str(sign.return_annotation)
      sig_str = '''{name}({params_str}){ret_str}'''.format(
        name=name, params_str=', '.join(p_strs), ret_str=ret_str)

      param_names = [p for p in sign.parameters]
      params_in_doc = set()
      for m in re.finditer('\`(\w)+\`', str(fn.__doc__)):
        params_in_doc.add(str(m.group(0))[1:-1])

      for param in params_in_doc:
        assert param in param_names, 'Param {param} is not in the signature of {name} ({param_names}).'.format(
          param=param, name=name, param_names=param_names)
      for param in param_names:
        assert param in params_in_doc or param in EXTRA_DOC_PARAMS, 'Param {param} of {name} is undocumented ({params_in_doc}).'.format(
          param=param, name=name, params_in_doc=params_in_doc)

      f.write('## {name}\n\n'.format(name=name))
      f.write('`{sig_str}`<br/>\n\n'.format(sig_str=sig_str))
      if fn.__doc__:
        doc_str = re.sub('(\s)+', ' ', str(fn.__doc__)).replace('<br>', '<br>\n')
        f.write('{doc_str}<br>\n\n'.format(doc_str=doc_str))
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
