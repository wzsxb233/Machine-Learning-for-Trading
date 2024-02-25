import numpy as np

class DTLearner(object):
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
            return np.array([[-1, np.mean(data[:, -1]), -1, -1]])
        else:
            corr = np.corrcoef(data, rowvar=False)[:-1,-1]
            corr = np.abs(corr)
            best_feature = np.argmax(corr)
            split_val = np.median(data[:, best_feature])
            
            if np.all(data[:, best_feature] <= split_val):  
                return np.array([[-1, np.mean(data[:, -1]), -1, -1]])
            else:
                left_data = data[data[:, best_feature] <= split_val]
                right_data = data[data[:, best_feature] > split_val]
                left_tree = self.build_tree(left_data)
                right_tree = self.build_tree(right_data)
                
                if right_tree.ndim == 1:
                    right_tree = np.expand_dims(right_tree, axis=0)

                root = np.array([[best_feature, split_val, 1, left_tree.shape[0] + 1]])
                return np.vstack((root, left_tree, right_tree))

    def query(self, points):
        preds = []
        for point in points:
            preds.append(self._traverse_tree(self.tree, point))
        return np.array(preds)

    def _traverse_tree(self, tree, point):
        feature = int(tree[0,0])
        if feature == -1:
            return tree[0,1]
        elif point[feature] <= tree[0,1]:
            left_tree = tree[1:int(tree[0,3]), :]
            return self._traverse_tree(left_tree, point)
        else:
            right_tree = tree[int(tree[0,3]):, :]
            return self._traverse_tree(right_tree, point)


