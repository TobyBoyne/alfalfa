import torch
import gpytorch as gpy
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

from alfalfa.tree_models.tree_kernels import AlfalfaGP
from alfalfa.tree_models.forest import AlfalfaForest
from alfalfa.fitting import BART, BARTData, BARTTrainParams
from alfalfa.utils.plots import plot_gp_2d
from alfalfa.utils.benchmarks import rescaled_branin
from alfalfa.leaf_gp.space import Space

torch.manual_seed(42)
np.random.seed(42)
N_train = 50
x = torch.rand((N_train, 2)) 
f = rescaled_branin(x)

y = f + torch.randn_like(f) * 0.2**0.5


likelihood = gpy.likelihoods.GaussianLikelihood(noise_constraint=gpy.constraints.Positive())
forest = AlfalfaForest(height=0, num_trees=30)
space = Space([[0.0, 1.0], [0.0, 1.0]])
forest.initialise(space)
gp = AlfalfaGP(x, y, likelihood, forest)


mll = gpy.mlls.ExactMarginalLogLikelihood(likelihood, gp)

output = gp(x)
loss = -mll(output, y)
print(f"Initial loss={loss}")

test_x = torch.rand((50, 2)) 
test_f = rescaled_branin(test_x)
test_y = test_f + torch.randn_like(test_f) * 0.2**0.5

data = BARTData(space, np.asarray(x))
params = BARTTrainParams(
    warmup_steps=500,
    n_steps=500,
    lag=500 // 5, # want 5 samples
)
bart = BART(gp, data, params, 
            scale_prior=stats.gamma(3.0, scale=1.94/3.0),
            noise_prior=stats.gamma(3.0, scale=0.057/3.0))
logger = bart.run()

output = gp(x)
loss = -mll(output, y)
print(f"Final loss={loss}")
gp.eval()

sampled_model = AlfalfaGP.from_mcmc_samples(gp, logger["samples"])
sampled_model.eval()


torch.save(sampled_model.state_dict(), "models/branin_sampled_bart_.pt")
test_x = torch.meshgrid(torch.linspace(0, 1, 50), torch.linspace(0, 1, 50), indexing="ij")
plot_gp_2d(sampled_model, test_x, target=rescaled_branin)
fig, axs = plt.subplots(nrows=2)
axs[0].plot(logger["noise"])
axs[1].plot(logger["scale"])
plt.show()
