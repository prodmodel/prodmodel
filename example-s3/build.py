from prodmodel.rules import rules


csv_data = rules.data_stream(
  file='s3://prodmodel-test/sources/data.csv',
  type='csv',
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
