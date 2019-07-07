import math


def average_age(data):
  ages = [math.ceil(row['age'] / 10) for row in data]
  return sum(ages) / len(ages)
