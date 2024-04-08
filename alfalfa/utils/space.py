import numpy as np
from beartype.cave import IntType
from beartype.typing import Generic, Optional, TypeVar

BoundType = int | float | str
B = TypeVar("B", int, float, str)


class Dimension(Generic[B]):
    var_type = ""
    is_bin = False

    def __init__(self, bnds: list[B], key: str):
        self.bnds = bnds
        self.key = key

    def __str__(self):
        return f"({self.var_type}, {self.bnds})"


class ContinuousDimension(Dimension[float]):
    var_type = "conti"

    def grid_sample(self, shape: IntType):
        ub, lb = self.bnds
        return np.linspace(ub, lb, shape)


class IntegerDimension(Dimension[int]):
    var_type = "int"

    @property
    def is_bin(self):
        return self.bnds == [0, 1]


class CategoricalDimension(Dimension[BoundType]):
    var_type = "cat"


class Space:
    def __init__(self, dims: list[Dimension]):
        self.cat_idx = [
            idx for idx, dim in enumerate(dims) if isinstance(dim, CategoricalDimension)
        ]
        self.int_idx = [
            idx for idx, dim in enumerate(dims) if isinstance(dim, IntegerDimension)
        ]
        self.cont_idx = [
            idx for idx in range(len(dims)) if idx not in self.cat_idx + self.int_idx
        ]
        self.dims = dims

        self._key_to_idx = {dim.key: idx for idx, dim in enumerate(self.dims)}

    @classmethod
    def from_bounds(
        cls,
        bnds: list[list[BoundType]],
        cat_idx: Optional[list[int]] = None,
        int_idx: Optional[list[int]] = None,
    ):
        cat_idx = cat_idx or []
        int_idx = int_idx or []

        dims = []
        for idx, b in enumerate(bnds):
            key = f"x{idx}"
            if idx in cat_idx:
                dims.append(CategoricalDimension(b, key))
            elif idx in int_idx:
                dims.append(IntegerDimension(b, key))
            else:
                dims.append(ContinuousDimension(b, key))

        return cls(dims)

    @property
    def bounds(self):
        return [d.bnds for d in self.dims]

    @property
    def keys(self):
        return [d.key for d in self.dims]

    def process_vals(self, X):
        pass

    def key_to_idx(self, keys: str | list[str]) -> int | list[int]:
        if isinstance(keys, str):
            return self._key_to_idx[keys]
        else:
            return [self._key_to_idx[k] for k in keys]

    def __getitem__(self, keys: str | list[str]):
        return self.key_to_idx(keys)

    def __str__(self):
        return str([str(d) for d in self.dims])

    def __len__(self):
        return len(self.dims)
