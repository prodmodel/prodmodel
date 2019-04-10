from feature_definitions import rich


def transform_record(record: dict, education_scores)-> dict:
  result = {}
  result.update(record)
  result['rich'] = rich(record)
  result['education_score'] = education_scores[record['education']]
  return result 
