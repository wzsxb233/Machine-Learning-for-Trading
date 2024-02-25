import numpy as np

class BagLearner:

    def __init__(self, learner, kwargs, bags=20, boost=False, verbose=False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []
        for _ in range(self.bags):
            self.learners.append(self.learner(**self.kwargs))

    def add_evidence(self, dataX, dataY):
        for learner in self.learners:
            indices = np.random.choice(dataX.shape[0], size=dataX.shape[0])
            sampleX, sampleY = dataX[indices], dataY[indices]
            learner.add_evidence(sampleX, sampleY)

    def query(self, points):
        predictions = np.array([learner.query(points) for learner in self.learners])
        return np.mean(predictions, axis=0)
    def author(self):
        return 'ydeng335'  
