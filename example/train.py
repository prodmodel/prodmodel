from sklearn import tree


def train(X, y):
  clf = tree.DecisionTreeClassifier(max_depth=5)
  clf = clf.fit(X, y)
  return clf
