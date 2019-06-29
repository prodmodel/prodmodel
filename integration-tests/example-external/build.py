from prodmodel.rules import rules

csv_data_scores = rules.external_data(
  file='sql_data.py',
  fn='load_table',
  args={
    'table': 'education_lookup'
  }
)
