import numpy as np

class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return 'ydeng335'  

    def add_evidence(self, data_x, data_y):
        data = np.column_stack((data_x, data_y)) 
        self.tree = self.build_tree(data)

    def build_tree(self, data):
        if data.shape[0] <= self.leaf_size:  
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])
        elif np.all(data[:, -1] == data[0, -1]):  
            return np.array([[-1, data[0, -1], np.nan, np.nan]])
        else:
            feature = np.random.randint(0, data.shape[1]-1)

            split_val = np.median(data[:, feature])
            if np.max(data[:, feature]) == split_val:  
                return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])
            else:
                left_tree = self.build_tree(data[data[:, feature] <= split_val])
                right_tree = self.build_tree(data[data[:, feature] > split_val])
                root = np.array([[feature, split_val, 1, left_tree.shape[0] + 1]])
                return np.concatenate((root, left_tree, right_tree), axis=0)

    def query(self, points):
        preds = []
        for point in points:
            preds.append(self.traverse(self.tree, point))
        return np.array(preds)

    def traverse(self, tree, point):
        if tree[0, 0] == -1:
            return tree[0, 1]
        else:
            if point[int(tree[0, 0])] <= tree[0, 1]:
                return self.traverse(tree[1:int(tree[0, 3]), :], point)
            else:
                return self.traverse(tree[int(tree[0, 3]):, :], point)
