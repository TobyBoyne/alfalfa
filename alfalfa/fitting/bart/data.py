"""Wrapper for data"""
import numpy as np

from ...forest import AlfalfaNode, AlfalfaTree, DecisionNode
from ...utils.space import Space


class Data:
    def __init__(self, space: Space, X: np.ndarray):
        self.space = space
        self.X = np.asarray(X)  # (N, D)

    def get_init_prior(self):
        def _prior(node: DecisionNode):
            var_idx, threshold = self.sample_splitting_rule(node.tree, node)
            node.var_idx = var_idx
            node.threshold = threshold

        return _prior

    def sample_splitting_rule(
        self, tree: AlfalfaTree, node: AlfalfaNode
    ) -> tuple[int, float]:
        x_index = self.get_x_index(tree, node)
        valid_features = self.valid_split_features(x_index)
        if not valid_features.size:
            # no valid splits to be made
            return
        var_idx = np.random.choice(valid_features)

        valid_values = self.unique_split_values(x_index, var_idx)
        # TODO: should endpoints be excluded for continuous variables?
        threshold = np.random.choice(valid_values)
        return var_idx, threshold

    def get_x_index(self, tree: AlfalfaTree, node: AlfalfaNode):
        """Get the index of datapoints that pass through the given node"""
        active_leaves = tree(self.X)
        return node.contains_leaves(active_leaves)

    def valid_split_features(self, x_index: np.ndarray):
        valid = [
            i
            for i in range(len(self.space))
            if len(self.unique_split_values(x_index, i)) >= 1
        ]
        return np.array(valid)

    def unique_split_values(self, x_index: np.ndarray, var_idx: int):
        """
        x_index is shape (N,), where it is true if the x value reaches a leaf"""
        x = self.X[x_index, var_idx]
        return np.unique(x)[1:]
