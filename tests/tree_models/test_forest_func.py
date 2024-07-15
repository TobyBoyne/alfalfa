import pyximport

pyximport.install()
from alfalfa.forest_func import pass_through_tree  # noqa: E402

print(pass_through_tree(1, 2))
