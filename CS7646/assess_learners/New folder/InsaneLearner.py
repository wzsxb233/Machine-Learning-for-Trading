import LinRegLearner as lrl
import BagLearner as bl

class InsaneLearner:
    def __init__(self, verbose=False):
        self.learner = bl.BagLearner(learner=bl.BagLearner, kwargs={"learner": lrl.LinRegLearner, "kwargs": {}, "bags": 20}, bags=20, boost=False, verbose=verbose)

    def add_evidence(self, dataX, dataY):
        self.learner.add_evidence(dataX, dataY)

    def query(self, points):
        return self.learner.query(points)
    def author(self):
        return 'ydeng335'  
