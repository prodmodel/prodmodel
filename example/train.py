from sklearn import tree


def train(X, y):
  clf = tree.DecisionTreeClassifier()
  clf = clf.fit(X, y)
  return clf
