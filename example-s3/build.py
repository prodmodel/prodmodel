from prodmodel.rules import aws_rules, rules

csv_data = rules.data_stream(
  file='s3://prodmodel-test/sources/data-small.csv',
  data_type='csv',
  dtypes = {
    'age': int,
    'job': str
  }
)

data_in_s3 = aws_rules.copy_to_s3(
  data=csv_data,
  s3_bucket='prodmodel-test',
  s3_key='dest/data-small.csv'
)
