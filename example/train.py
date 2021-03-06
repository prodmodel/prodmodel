from sklearn import tree


def train(X, y):
  clf = tree.DecisionTreeClassifier(max_depth=10, random_state=0)
  clf = clf.fit(X, y)
  return clf
