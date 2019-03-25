import rules


csv_data = rules.data_source(
  file='example/data.csv',
  type='csv',
  dtypes = {
    'age':int,
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
  target_column='y'
)

enriched_train_data_x = rules.transform(
  data=train_data_x,
  file='example/transform_record.py'
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
  file='example/train.py'
)

'''
predict = rules.predict(
  file='predict.py'
)

enriched_test_data = rules.transform(
  data=test_data,
  file='transform_record.py'
)

final_test_data = rules.encode_labels(
  data=enriched_test_data,
  label_encoder=label_encoder
)

evaluate = rules.evaluate(
  model=model,
  data=final_test_data,
  predict=predict,
  file='evaluate_results.py'
)
'''
