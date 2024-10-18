from dataclasses import dataclass
from itertools import chain
from pprint import pprint



# coins [2, 3]
# 4: [2, 2]
# 5: [2, 3]
# 6: [3, 3]
# 7: [2, 2, 3]
# 8: [2, 3, 3]
# 9: [3, 3, 3]
# 10: [2, 2, 3, 3]
# 11: [2, 3, 3, 3]
# 12: [3, 3, 3, 3]
# 13: [2, 2, 3, 3, 3]
# 14: [2, 3, 3, 3, 3]

# Next iteration: find a python package that provides tree ops

def find_fewest_coins(coins, target):
    if target < 0:
        raise ValueError("target can't be negative")
    tree = build_tree(coins, target)
    leaf_nodes = get_leaf_nodes(tree)
    paths = [get_lineage(n) for n in leaf_nodes]
    paths = [p for p in paths if get_path_total(p) == target]
    if not paths:
        raise ValueError("can't make target with given coins")
    best_path = min(paths, key=get_coin_count)
    return get_coin_list(best_path)


@dataclass
class Node:
    denom: int
    count: int
    target: int
    children: list['Node']
    parent: 'Node' = None

    def __repr__(self):
        return f"Node({self.denom=},{self.count=})"

    def add_children(self, denoms, target):
        for d in denoms:
            count, remainder = divmod(target, d)
            if count > 0:
                child = Node(d, count, remainder, [])
                child.parent = self
                self.children.append(child)
                child.add_children(denoms, remainder)

def build_tree(denoms, target):
    root = Node(0, 0, target, [])
    root.add_children(denoms, target)
    return root

def get_leaf_nodes(node):
    result = []
    for c in node.children:
        result += get_leaf_nodes(c)
    if not node.children:
        result += [node]
    return result

def get_lineage(node):
    result = [node] if node.count else []
    if node.parent:
        result += get_lineage(node.parent)
    return result

def get_path_total(path):
    return sum(n.count * n.denom for n in path)
    
def get_coin_count(path):
    return sum(n.count for n in path)

def get_coin_list(path):
    result = []
    for node in path:
        result += [node.denom] * node.count
    return result
