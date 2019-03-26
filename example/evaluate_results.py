def evaluate(predicted_y, test_y):
  n = 0
  good = 0
  for p_y, t_y in zip(predicted_y, test_y):
    t_y = t_y[0]
    if p_y == t_y:
      good = good + 1
    n = n + 1
  return {'accuracy': (good / n), 'num_samples': n}
