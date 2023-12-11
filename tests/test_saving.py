import pytest
import gpytorch as gpy

from alfalfa.alternating.alternating_forest import AlternatingTree, AlternatingForest
from alfalfa.alternating.af_kernel import AFGP

def test_saving_and_loading_alternating_tree():
    tree = AlternatingTree(depth=2)
    state = tree.state_dict()

    model = AlternatingTree(depth=2)
    model.load_state_dict(state)

def test_saving_and_loading_alternating_forest():
    forest = AlternatingForest(depth=2, num_trees=5)
    state = forest.state_dict()

    model = AlternatingForest(depth=2, num_trees=5)
    model.load_state_dict(state)

def test_saving_and_loading_afgp():
    forest = AlternatingForest(depth=2, num_trees=5)
    gp = AFGP(None, None, gpy.likelihoods.GaussianLikelihood(), forest)
    state = gp.state_dict()

    forest = AlternatingForest(depth=2, num_trees=5)
    gp = AFGP(None, None, gpy.likelihoods.GaussianLikelihood(), forest)
    gp.load_state_dict(state)


