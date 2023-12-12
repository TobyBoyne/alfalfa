"""Convert an LGBM tree to an instance of Alternating Tree for comparison"""
import torch
import gpytorch as gpy
import lightgbm as lgb

from alfalfa.alternating.alternating_forest import Node, AlternatingTree, Leaf, AlternatingForest
from alfalfa.leaf_gp.lgbm_processing import order_tree_model_dict
from alfalfa.leaf_gp.gbm_model import GbmModel

def lgbm_to_alfalfa_forest(tree_model):
    """Convert a lightgbm model to an alternating forest"""
    original_tree_model_dict = tree_model.dump_model()
    ordered_tree_model_dict = \
        order_tree_model_dict(original_tree_model_dict)
    
    def get_subtree(tree, i=0):
        node_dict = tree[i]
        if node_dict["split_var"] != -1:
            left, i = get_subtree(tree, i+1)
            right, i = get_subtree(tree, i)
            return Node(
                var_idx=node_dict["split_var"],
                threshold=node_dict["split_code_pred"],
                left=left,
                right=right
            ), i
        else:
            return Leaf(), i+1

    trees = []
    for tree in ordered_tree_model_dict:
        root, _ = get_subtree(tree)
        trees.append(AlternatingTree(root=root))

    return AlternatingForest(trees=trees)