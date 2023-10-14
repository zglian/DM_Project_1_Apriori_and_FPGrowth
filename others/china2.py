from functools import reduce
from collections import Counter, defaultdict
from typing import DefaultDict, Dict, List, Tuple
from itertools import combinations

class Node(object):
    def __init__(self, name, fa) -> None:
        self.name = name
        self.fa = fa
        self.children = []
        self.children_name = []

        self.__count = 1
    
    def add_count(self):
        self.__count += 1
    
    @property
    def count(self):
        return self.__count

# reture True and path if tree only has only one path
def get_single_path(root : Node) -> Tuple[bool, List[Node]]:
    cur_node = root
    path = []
    while True:
        if cur_node.name != 'root':
            path.append(cur_node)
        if len(cur_node.children) == 0:
            return True, path
        elif len(cur_node.children) == 1:
            cur_node = cur_node.children[0]
        else:
            return False, []

def all_combination(array) -> list:
    for i, _ in enumerate(array):
        for elements in combinations(array, i + 1):
            yield list(elements)

# return root of a constructed fp-tree
# return root and item table
def build_FP_tree(itemsets : List[List[str]], n_sup : int) -> Tuple[Node, Dict]:
    # two rounds of scanning : count and build
    counter = Counter(reduce(lambda x, y : x + y, itemsets))
    item_table = sorted(counter, key=lambda x : counter[x])
    item_table = {item : {'count' : counter[item], 'node' : []} for item in item_table if counter[item] >= n_sup}

    root = Node('root', None)
    for itemset in itemsets:
        cur_fa_node = root
        itemset = sorted((item for item in itemset if counter[item] >= n_sup), key=lambda x : counter[x], reverse=True)
        for item in itemset:
            if item in cur_fa_node.children_name:
                i = cur_fa_node.children_name.index(item)
                cur_fa_node : Node = cur_fa_node.children[i]
                cur_fa_node.add_count()
            else:
                new_node = Node(item, cur_fa_node)
                cur_fa_node.children_name.append(item)
                cur_fa_node.children.append(new_node)
                cur_fa_node = new_node
            
            # node is trimmed and the first layer of the tree is trimmed too
            # because the nodes in the first layer don't have CPB
            if cur_fa_node.name != 'root' and cur_fa_node.fa.name != 'root':
                item_table[item]['node'].append(cur_fa_node)
    
    return root, item_table

# CPB : conditional pattern base
def find_CPB(item_table : Dict, item_name : str) -> List[List[str]]:
    cpb = []
    # for optimization
    log = {}
    for node in item_table[item_name]['node']:
        if node not in log:
            suffix = []
            cur_node : Node = node.fa
            while cur_node.name != 'root':
                suffix.append(cur_node.name)
                cur_node = cur_node.fa
            if suffix:
                log[node] = suffix
            else:
                continue
        cpb.append(log[node][:])

    return cpb

def FP_growth(root: Node, item_table: Dict, alpha: List[str], n_sup: int, result: DefaultDict[str, set], support_dict: Dict[str, int]):
    ret, path = get_single_path(root)
    if ret:  # have one path
        for each_combination in all_combination(path):
            # generate pattern
            pattern = alpha + [node.name for node in each_combination]
            result[alpha[0]].add(tuple(pattern))
            # Calculate and store support for the pattern
            support = min(node.count for node in each_combination)
            support_dict[tuple(pattern)] = support
    else:
        for item_name in item_table:
            # generate pattern, alpha[0] is the domain name
            pattern = alpha + [item_name]
            if alpha:
                result[alpha[0]].add(tuple(pattern))
            # generate sub dataset, which is conditional pattern base
            sub_itemsets = find_CPB(item_table, item_name)
            if sub_itemsets:
                sub_root, sub_item_table = build_FP_tree(sub_itemsets, n_sup)
                if sub_root.children:
                    FP_growth(sub_root, sub_item_table, pattern, n_sup, result, support_dict)

def FPGrowth(transaction: dict, min_sup: float) -> Dict[str, Tuple[List[List[str]], Dict[Tuple[str], int]]]:
    n_sup = round(min_sup * len(transaction))
    root, itemtable = build_FP_tree(list(transaction.values()), n_sup)

    result = defaultdict(set)
    support_dict = {}  # Dictionary to store support for each itemset

    FP_growth(root, itemtable, [], n_sup, result, support_dict)

    # Convert result sets to lists
    for item, itemsets in result.items():
        result[item] = [list(itemset) for itemset in itemsets]

    return dict(result), support_dict

transactions = {
    'T100': ['I1', 'I2', 'I3'],
    'T200': ['I2', 'I4'],
    'T300': ['I2', 'I5'],
    'T400': ['I1', 'I2', 'I4'],
    'T500': ['I1', 'I5'],
    'T600': ['I2', 'I5'],
    'T700': ['I1', 'I5'],
    'T800': ['I1', 'I2', 'I3', 'I5'],
    'T900': ['I1', 'I2', 'I5']
}

if __name__ == "__main__":
    frequent_itemsets, support_dict = FPGrowth(transactions, 2 / 9)

    for item, itemsets in frequent_itemsets.items():
        print(f"Frequent {item} itemsets:")
        for itemset in itemsets:
            support = support_dict[tuple(itemset)]
            print(f"Itemset: {itemset}, Support: {support}")