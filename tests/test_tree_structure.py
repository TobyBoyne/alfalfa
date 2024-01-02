from alfalfa.tree_models.forest import AlfalfaTree, Node, Leaf

def test_tree_structure_equals():
    tree1 = Node(var_idx=0, threshold=0.5, left=Leaf(), right=Leaf())

    tree2 = Node(var_idx=0, threshold=0.5, left=Leaf(), right=Leaf())

    tree3 = Node(
        var_idx=0, threshold=0.5,
        left=Leaf(),
        right=Node(var_idx=1, threshold=1.0, left=Leaf(), right=Leaf())
    )

    assert tree1.structure_eq(tree2)
    assert not tree1.structure_eq(tree3)