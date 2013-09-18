__author__ = 'jeongmingi'

#/sw_maestro_data_mining/Min/utils/svm(NAIVE, SVC_gen_view)/SVC_params_gender_graph.txt
#/sw_maestro_data_mining/Min/utils/view by plot_2D.txt

%pylab inline

import pylab as pl
def plot_2D(data, target, target_names):
    colors = cycle('rgbcmykw')
    target_ids = range(len(target_names))
    pl.figure()
    for i, c, label in zip(target_ids, colors, target_names):
        pl.scatter(data[target == i, 0], data[target == i, 1],
                   c=c,a label=label)
    pl.legend()

from sklearn.cross_validation import ShuffleSplit
from sklearn.svm import SVC
import numpy as np
#import pylab as pl


n_Cs = 10
n_iter = 5
cv = ShuffleSplit(n_samples, n_iter=n_iter, train_size=500, test_size=500,
    random_state=0)

train_scores = np.zeros((n_Cs, n_iter))
test_scores = np.zeros((n_Cs, n_iter))
Cs = np.logspace(-5, 5, n_Cs)

for i, C in enumerate(Cs):
    for j, (train, test) in enumerate(cv):
        clf = SVC(C=C, gamma=1e-4).fit(X[train], y[train])
        train_scores[i, j] = clf.score(X[train], y[train])
        test_scores[i, j] = clf.score(X[test], y[test])



for i in range(n_iter):
    pl.semilogx(Cs, train_scores[:, i], alpha=0.4, lw=2, c='b')
    pl.semilogx(Cs, test_scores[:, i], alpha=0.4, lw=2, c='g')
pl.ylabel("score for SVC(C=C, gamma=1e-3)")
pl.xlabel("C")
pl.text(1e-3, 0.5, "Underfitting", fontsize=16, ha='center', va='bottom')
pl.text(1e3, 0.5, "Few Overfitting", fontsize=16, ha='center', va='bottom')
pl.show()
