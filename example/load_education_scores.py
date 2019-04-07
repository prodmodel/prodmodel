def transform(csv):
  print(csv)
  values = {}
  for record in csv:
    values[record['education']] = record['score']
  return values
