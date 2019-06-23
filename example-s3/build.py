from prodmodel.rules import aws_rules, rules

csv_data = rules.data_stream(
  file='s3://prodmodel-test/sources/data.csv',
  data_type='csv',
  dtypes = {
    'age': int,
    'job': str,
    'marital': str,
    'education': str,
    'default': str,
    'balance': int,
    'housing': str,
    'loan': str,
    'contact':str,
    'day':int,
    'month':str,
    'duration':int,
    'campaign':int,
    'pdays':int,
    'previous':int,
    'poutcome':str,
    'y':str
  }
)

data_in_s3 = aws_rules.copy_to_s3(
  data=csv_data,
  s3_bucket='prodmodel-test',
  s3_key='data/data.csv'
)
