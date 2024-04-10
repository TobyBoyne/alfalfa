import gpytorch as gpy
import matplotlib.pyplot as plt
import scipy.stats as stats
import torch
from jaxtyping import install_import_hook

with install_import_hook("alfalfa", "beartype.beartype"):
    from alfalfa.fitting import BART, BARTData, BARTTrainParams
    from alfalfa.forest import AlfalfaForest
    from alfalfa.tree_kernels import AlfalfaGP, AlfalfaSampledModel
    from alfalfa.utils.metrics import nlpd
    from alfalfa.utils.plots import plot_gp_nd

import problem

likelihood = gpy.likelihoods.GaussianLikelihood(
    noise_constraint=gpy.constraints.Positive()
)
forest = AlfalfaForest(height=0, num_trees=20)
space = problem.bb_func.space
forest.initialise(space)
gp = AlfalfaGP(problem.train_x_torch, problem.train_y_torch, likelihood, forest)


mll = gpy.mlls.ExactMarginalLogLikelihood(likelihood, gp)

output = gp(problem.train_x_torch)
loss = -mll(output, problem.train_y_torch)
print(f"Initial loss={loss}")

data = BARTData(space, problem.train_x_np)
params = BARTTrainParams(
    warmup_steps=10,
    n_steps=10,
    lag=1,
)
bart = BART(
    gp,
    data,
    params,
    scale_prior=stats.halfnorm(scale=1.0),
    noise_prior=stats.halfnorm(scale=1.0),
)
logger = bart.run()

output = gp(problem.train_x_torch)
loss = -mll(output, problem.train_y_torch)
print(f"Final train loss={loss}")
gp.eval()

output = gp(problem.test_x_torch)
test_loss = nlpd(output, problem.test_y_torch, diag=True)
print(f"Final test loss={test_loss}")


sampled_model = AlfalfaSampledModel(
    problem.train_x_torch,
    problem.train_y_torch,
    logger["samples"],
    space,
    sampling_seed=100,
)

output = sampled_model(problem.train_x_torch)
loss = -mll(output, problem.train_y_torch)
print(f"Final train loss={loss}")

output = sampled_model(problem.test_x_torch)
test_loss = nlpd(output, problem.test_y_torch, diag=True)
print(f"Final test loss={test_loss}")


test_x = torch.meshgrid(
    torch.linspace(0, 1, 25), torch.linspace(0, 1, 25), indexing="ij"
)

plot_gp_nd(gp, test_x, target=problem.bb_func.vector_apply)
plot_gp_nd(sampled_model, test_x, target=problem.bb_func.vector_apply)

fig, axs = plt.subplots(nrows=2)
axs[0].plot(logger["noise"])
axs[1].plot(logger["scale"])
plt.show()
