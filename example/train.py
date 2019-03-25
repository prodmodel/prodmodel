from sklearn import tree


def train(X, y):
  clf = tree.DecisionTreeClassifier()
  clf = clf.fit(X, y)
  print(X)
  print(y)
  return clf
