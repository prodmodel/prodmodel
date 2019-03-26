def evaluate(predicted_y, test_y):
  n = 0
  s = 0
  for p_y, t_y in zip(predicted_y, test_y):
    s = s + (p_y - t_y) * (p_y - t_y)
    n = n + 1
  return s / n
