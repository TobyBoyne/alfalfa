from beartype.typing import Union

from .base import CatSynFunc, DatasetFunc, SynFunc, standardise
from .constrained import G1, G3, G4, G6, G7, G10, Alkylation
from .dataset import (
    Abalone,
    AutoMPG,
    ConcreteCompressive,
    JsonDatasetFunc,
    StudentPerformance,
)
from .mixed import CatAckley, PressureVessel, VAESmall
from .multi_fidelity import CurrinExp2D
from .pest import PestControl
from .unconstrained import (
    Branin,
    CombinationFunc2,
    Friedman,
    Hartmann6D,
    Himmelblau1D,
    OrthogonalRosenbrock,
    Rastrigin,
    Schwefel,
    StyblinskiTang,
)
from .xgboost_mnist import XGBoostMNIST

BENCHMARK_MAP = {
    # unconstrained spaces
    "hartmann6d": Hartmann6D,
    "himmelblau1d": Himmelblau1D,
    "branin": Branin,
    "friedman": Friedman,
    "rastrigin": Rastrigin,
    "styblinski_tang": StyblinskiTang,
    "schwefel": Schwefel,
    "combination_func2": CombinationFunc2,
    "ortho_ros": OrthogonalRosenbrock,
    # constrained spaces
    "g1": G1,
    "g3": G3,
    "g4": G4,
    "g6": G6,
    "g7": G7,
    "g10": G10,
    "alkylation": Alkylation,
    # mixed spaces
    "pest": PestControl,
    "pressure_vessel": PressureVessel,
    "vae_nas": VAESmall,
    "cat_ackley": CatAckley,
    # multi-fidelity
    "currin": CurrinExp2D,
    # datasets
    "auto_mpg": AutoMPG,
    "student_performance": StudentPerformance,
    "abalone": Abalone,
    "concrete": ConcreteCompressive,
    "json": JsonDatasetFunc,
    "xgboost": XGBoostMNIST,
}


def map_benchmark(name: str, **kwargs) -> Union[SynFunc, CatSynFunc, DatasetFunc]:
    """Map a benchmark name to a function that generates the benchmark

    Args:
        name (str): the name of the benchmark
        **kwargs: additional arguments to pass to the benchmark function

    Returns:
        Union[SynFunc, CatSynFunc, DatasetFunc]: the benchmark function
    """
    return BENCHMARK_MAP[name](**kwargs)
