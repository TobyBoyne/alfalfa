import numpy as np
import torch
from jaxtyping import install_import_hook

with install_import_hook("alfalfa", "beartype.beartype"):
    from alfalfa.benchmarks import Branin


torch.set_default_dtype(torch.float64)
torch.manual_seed(42)
np.random.seed(42)

NOISE_VAR = 0.2

bb_func = Branin(seed=42)
train_x_np, train_f_np = bb_func.get_init_data(50, rnd_seed=42)
train_y_np = train_f_np + np.random.randn(*train_f_np.shape) * NOISE_VAR**0.5

train_x_torch, train_f_torch, train_y_torch = map(
    torch.as_tensor, (train_x_np, train_f_np, train_y_np)
)
