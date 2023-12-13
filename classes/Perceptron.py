import numpy as np
import random

class Perceptron:
    def __init__(self, lr=0.01, n_iter=50, random_state=1):
        self._lr = lr
        self._n_iter = n_iter
        self._rand_state = random_state
        self._errors = list()
        return
    
    def reset(self):
        self._errors.clear()
        return

    def fit(self, X, y):
        self.reset()

        rgen = np.random.RandomState(self._rand_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=X.shape[1])
        self.b_ = np.float_(0.)

        for _ in range(self._n_iter):
            curr_error = 0
            for xi, y_i in zip(X, y):
                update = self._lr * (y_i - self.predict(xi))
                self.w_ += update * xi
                self.b_ += update
                curr_error += int(update != 0.0)
            self._errors.append(curr_error)
            print(self.w_)

        return

    def net_input(self, X):
        return np.dot(X, self.w_) + self.b_

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, 0)

    