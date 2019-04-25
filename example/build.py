from rules import rules
from rules import aws_rules


rules.requirements(
  packages=['sklearn']
)


csv_data_scores = rules.external_data(
  file='sql_data.py',
  fn='load_table',
  args={
    'table': 'education_lookup'
  }
)

education_scores = rules.transform(
  objects={'csv': csv_data_scores},
  file='load_education_scores.py',
  fn='transform'
)

csv_data = rules.data_source(
  file='data.csv',
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


train_data_x, train_data_y, test_data_x, test_data_y = rules.split(
  data=csv_data,
  test_ratio=0.2,
  target_column='y',
  seed=3
)

feature_definitions = ['feature_definitions.py']

enriched_train_data_x = rules.transform_stream(
  stream=train_data_x,
  objects={'education_scores': education_scores},
  file='transform_record.py',
  fn='transform_record',
  file_deps=feature_definitions
)

label_encoder_x = rules.create_label_encoder(
  data=enriched_train_data_x,
  columns=['job','marital','education','default','housing','loan','contact','month','poutcome']
)

label_encoder_y = rules.create_label_encoder(
  data=train_data_y,
  columns=['y']
)

final_train_data_x = rules.encode_labels(
  data=enriched_train_data_x,
  label_encoder=label_encoder_x
)

final_train_data_y = rules.encode_labels(
  data=train_data_y,
  label_encoder=label_encoder_y
)

model = rules.transform(
  objects={
      'X': final_train_data_x,
      'y': final_train_data_y
  },
  file='train.py',
  fn='train'
)


enriched_test_data_x = rules.transform_stream(
  stream=test_data_x,
  objects={'education_scores': education_scores},
  file='transform_record.py',
  fn='transform_record'
)

final_test_data_x = rules.encode_labels(
  data=enriched_test_data_x,
  label_encoder=label_encoder_x
)

test_predictions = rules.transform(
  objects={
      'model': model,
      'data': final_test_data_x
  },
  file='predict.py',
  fn='predict'
)

final_test_data_y = rules.encode_labels(
  data=test_data_y,
  label_encoder=label_encoder_y
)

evaluate = rules.transform(
  objects={
      'test_y': final_test_data_y,
      'predicted_y': test_predictions
  },
  file='evaluate_results.py',
  fn='evaluate'
)

test_transform = rules.test(
  test_file='tests/test_transform_record.py',
  file_deps=['transform_record.py'] + feature_definitions
)

model_in_s3 = aws_rules.copy_to_s3(
  data=model,
  s3_bucket='prodmodel-test',
  s3_key='models/model1.pickle'
)
