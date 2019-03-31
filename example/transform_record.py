def _rich(record):
  if record['marital'] == 'single':
    return record['balance'] >= 500
  else:
    return record['balance'] >= 1000


def transform_record(record: dict, education_scores)-> dict:
  result = {}
  result.update(record)
  result['rich'] = _rich(record)
  result['education_score'] = education_scores[record['education']]
  return result 
