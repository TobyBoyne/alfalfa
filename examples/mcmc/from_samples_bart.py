import math

import gpytorch
import numpy as np
import scipy.stats as stats
import torch
from matplotlib import pyplot as plt

from alfalfa.fitting.bart.bart import BART
from alfalfa.fitting.bart.data import Data
from alfalfa.fitting.bart.params import BARTTrainParams
from alfalfa.forest import AlfalfaForest
from alfalfa.tree_kernels import AlfalfaGP
from alfalfa.utils.plots import plot_gp_1d
from alfalfa.utils.space import Space

# Training data is 11 points in [0,1] inclusive regularly spaced
train_x = torch.linspace(0, 1, 10).reshape(-1, 1)
space = Space([[0.0, 1.0]])

# True function is sin(2*pi*x) with Gaussian noise
torch.manual_seed(42)
np.random.seed(42)


def f(x):
    return torch.sin(x * (2 * math.pi))


train_y = (f(train_x) + torch.randn(train_x.size()) * 0.2).flatten()

tree = AlfalfaForest(height=0, num_trees=10)
data = Data(space, train_x)
tree.initialise(space, data.get_init_prior())
likelihood = gpytorch.likelihoods.GaussianLikelihood(
    noise_constraint=gpytorch.constraints.Positive()
)
model = AlfalfaGP(train_x, train_y, likelihood, tree)

params = BARTTrainParams(warmup_steps=50)
bart = BART(model, data, params, scale_prior=stats.halfnorm(scale=5.0))
logger = bart.run()

model.eval()
# torch.save(model.state_dict(), "models/1d_bart.pt")
sampled_model = AlfalfaGP.from_mcmc_samples(model, logger["samples"])
sampled_model.eval()

test_x = torch.linspace(0, 1, 100).reshape(-1, 1)
fig, ax = plot_gp_1d(sampled_model, test_x, f)
fig, axs = plt.subplots(ncols=3)
axs[0].plot(logger["noise"])
axs[1].plot(logger["scale"])
with torch.no_grad():
    cov = sampled_model.covar_module(test_x).evaluate().numpy()
axs[2].imshow(cov, interpolation="nearest")

plt.show()
