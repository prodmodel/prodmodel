import rules

rules.requirements(
  packages=['sklearn']
)

csv_data_scores = rules.data_source(
  file='education_lookup.csv',
  type='csv',
  dtypes = {
    'education': str,
    'score': int
  }
)

education_scores = rules.transform(
  streams={'csv': csv_data_scores},
  file='csv_to_dict.py'
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

enriched_train_data_x = rules.transform_stream(
  stream=train_data_x,
  objects={'education_scores': education_scores},
  file='transform_record.py'
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

model = rules.train(
  features_data=final_train_data_x,
  labels_data=final_train_data_y,
  file='train.py'
)


enriched_test_data_x = rules.transform_stream(
  stream=test_data_x,
  objects={'education_scores': education_scores},
  file='transform_record.py'
)

final_test_data_x = rules.encode_labels(
  data=enriched_test_data_x,
  label_encoder=label_encoder_x
)

test_predictions = rules.predict(
  model=model,
  data=final_test_data_x,
  file='predict.py'
)

final_test_data_y = rules.encode_labels(
  data=test_data_y,
  label_encoder=label_encoder_y
)

evaluate = rules.evaluate(
  labels_data=final_test_data_y,
  predictions_data=test_predictions,
  file='evaluate_results.py'
)

