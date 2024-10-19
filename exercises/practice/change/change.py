from dataclasses import dataclass

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
    return sorted(get_coin_list(best_path))


@dataclass
class Node:
    denom: int
    count: int
    target: int
    children: list['Node']
    parent: 'Node' = None

    def add_children(self, denoms, target):
        for d in reversed(denoms):
            count = target // d
            if count > 0:
                if len(denoms) > 1:
                    for c in reversed(range(1, count+1)):
                        child = self.add_child(d, c, target)
                        if child.target:
                            child.add_children(denoms[:-1], child.target)
                        else:
                            break
                else:
                    self.add_child(d, count, target)

    def add_child(self, denom, count, target):
        remainder = target - count * denom
        child = Node(denom, count, remainder, [], self)
        self.children.append(child)
        return child


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
