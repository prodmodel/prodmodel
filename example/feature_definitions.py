def rich(record):
  if record['marital'] == 'single':
    return record['balance'] >= 500
  else:
    return record['balance'] >= 1000
