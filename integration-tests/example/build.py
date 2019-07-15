from pathlib import Path

from prodmodel.rules import rules


csv_data = rules.data_stream(
  file='data.csv',
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

csv_data_to_json = rules.data_stream(
  file='data.csv',
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
  },
  output_format='json'
)

csv_data_file = rules.data_file(
  file='data.csv',
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

shape_file = rules.data_file(
  file='countries/ne_50m_admin_0_countries',
  data_type='shp'
)

average_age = rules.transform(
  file='util_functions.py',
  fn='average_age',
  objects={'data': csv_data_to_json},
)

deploy_json = rules.deploy_target(
  data=csv_data_to_json,
  deploy_path=str(Path.home() / 'deployed.json')
)
