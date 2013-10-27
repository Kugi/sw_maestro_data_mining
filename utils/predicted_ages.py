__author__ = 'jeongmingi'


from sklearn.svm import LinearSVC
import numpy as np
from sklearn.cross_validation import ShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split

from sklearn.datasets import load_svmlight_file
X, y = load_svmlight_file("data/user_age.dat")
#c = 0
for i, np in enumerate(y):
    if ((np > 3.) and (np < 4.)):
        y[i] = 3.;
    elif(np>=4.):
        y[i] = 4.
    else:
        pass

n_samples, n_features = X.shape

n_Cs = 10
n_iter = 5
n_samples, n_features = X.shape
n_samples = 5000

cv = ShuffleSplit(n_samples, n_iter=n_iter,
                  test_size=0.2, random_state=0)

train_scores = np.zeros((n_Cs, n_iter))
test_scores = np.zeros((n_Cs, n_iter))
Cs = np.logspace(-7, 2, n_Cs)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=0)

Lparam = {
    'C': np.logspace(-5, 1, 15),
    }

gcv = GridSearchCV(LinearSVC(), Lparam, cv=3, n_jobs=-1)
gcv.fit(X_train, y_train)
print gcv.best_params_, gcv.best_score_