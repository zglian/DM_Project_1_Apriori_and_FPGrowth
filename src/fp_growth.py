from functools import reduce
from collections import Counter, defaultdict
from typing import DefaultDict, Dict, List, Tuple
from itertools import combinations
import argparse
import csv
import time

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

def build_FPtree(itemsets : List[List[str]], n_sup : int) -> Tuple[Node, Dict]:
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
            if cur_fa_node.name != 'root' and cur_fa_node.fa.name != 'root':
                item_table[item]['node'].append(cur_fa_node)
    
    return root, item_table


def find_CPB(item_table : Dict, item_name : str) -> List[List[str]]:
    cpb = []
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

def FP_growth(root : Node, item_table : Dict, alpha : List[str], n_sup : int, result : DefaultDict[str, set]):
    ret, path = get_single_path(root)
    if ret:    
        # if alpha:  # Check if alpha is not empty before accessing alpha[0]
        #      result[alpha[0]].add(tuple(alpha))
        for each_combination in all_combination(path):
            pattern = alpha + [node.name for node in each_combination]
            # if result is None:
            #     continue
            if alpha:
                result[alpha[0]].add(tuple(pattern))
    else:
        for item_name in item_table:
            pattern = alpha + [item_name]
            if alpha:
                result[alpha[0]].add(tuple(pattern))
            sub_itemsets = find_CPB(item_table, item_name)
            if sub_itemsets:
                sub_root, sub_item_table = build_FPtree(sub_itemsets, n_sup)
                if sub_root.children:
                    FP_growth(sub_root, sub_item_table, pattern, n_sup, result)


def FPGrowth(transaction : dict, min_sup : float) -> Dict[str, List[List[str]]]:
    n_sup = round(min_sup * len(transaction))
    root, itemtable = build_FPtree(list(transactions.values()), n_sup)
    result = defaultdict(set)
    FP_growth(root, itemtable, [], n_sup, result)

    for item, itemsets in result.items():
        result[item] = [list(itemset) for itemset in itemsets]

    return dict(result)

transactions = {}
header_table = {}

def read_dataset(filename):
    with open(filename, "r") as file:
        for line in file:
            parts = line.split()
            #customer_id = int(parts[0])
            transaction_id = parts[1]
            item_id = [parts[2]]
            
            if transaction_id in transactions:
                transactions[transaction_id].extend(item_id)
            else:
                transactions[transaction_id] = item_id

def write_to_csv(association_rules, output_file):
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['antecedent', 'consequent', 'support', 'confidence', 'lift'])
        for rule in association_rules:
            antecedent = "[{}]".format(', '.join([f"'{item}'" for item in map(str, rule[0])]))
            consequent = "[{}]".format(', '.join([f"'{item}'" for item in map(str, rule[1])]))
            support = round(rule[2], 2)
            confidence = round(rule[3], 2)
            lift = round(rule[4], 2)
            csv_writer.writerow([antecedent, consequent, support, confidence, lift])

def build_header_table(filename):
    transactions = defaultdict(list)
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            transaction_id = int(parts[1])
            item_id = int(parts[2])
            transactions[transaction_id].append(item_id)

    dataset = list(transactions.values())
    for transaction in dataset:
        for item in transaction:
            if item in header_table:
                header_table[item][0] += 1
            else:
                header_table[item] = [1, None]
    return dataset

def generate_rules(list_result, dataset, min_sup, min_conf):
    frequent_itemset = []
    rules = []
    for itemset in list_result:
        count = calculate_count(itemset, dataset)
        frequent_itemset.append((itemset, count))
    
    for itemset, count in frequent_itemset:
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = set(antecedent)
                consequence = set(item for item in itemset if item not in antecedent)
                support_antecedent = calculate_support(antecedent, frequent_itemset)
                support_consequence = calculate_support(consequence, frequent_itemset)
                support_itemset = count / length
                confidence = support_itemset / support_antecedent
                lift = support_itemset / (support_antecedent * support_consequence)
                if confidence >= min_conf:
                    rules.append((antecedent, consequence, support_itemset, confidence, lift))
    return rules

def calculate_count(itemset, dataset):
    count = 0
    itemset = set(itemset)
    for transaction_set in dataset:\
    
        if itemset.issubset(transaction_set):
            count += 1
    return count 

def calculate_support(itemset, frequent_itemset):
    count = 0
    temp = itemset
    if len(itemset) == 1:
        count = header_table[ int(next(iter(itemset)))][0]
        return count / length
    for frequent_item, frequent_count in frequent_itemset:
        frequent_item = set(frequent_item)
        if itemset == frequent_item:
            count += frequent_count
            return count / length

if __name__ == "__main__":
    # test_args={
    #     "dataset": "ibm-2023.txt",
    #     "min_sup": 0.1,
    #     "min_conf": 0.1
    # }
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type = str, required = True)
    parser.add_argument("--min_sup", type = float, required = True)
    parser.add_argument("--min_conf", type = float, required = True)
    # parser.add_argument("--dataset", type=str, default=test_args["dataset"])
    # parser.add_argument("--min_sup", type=float, default=test_args["min_sup"])
    # parser.add_argument("--min_conf", type=float, default=test_args["min_conf"])
    args = parser.parse_args()

    start_time = time.time()

    dataset_path = f'./inputs/{args.dataset}'
    read_dataset(dataset_path)
    dataset = build_header_table(dataset_path)
    length = len(dataset)

    result = FPGrowth(transactions, args.min_sup)
    list_result = []
    for item, itemsets in result.items():
        for itemset in itemsets:
            list_result.append(itemset)
    converted_list_result = [[int(item) for item in sublist] for sublist in list_result]
    rules = generate_rules(converted_list_result, dataset, args.min_sup, args.min_conf)
    output_file = f'outputs/{args.dataset.replace(".txt", "-fp_growth")}-{args.min_sup}-{args.min_conf}.csv'
    write_to_csv(rules, output_file)

    end_time = time.time()
    execution_time = end_time - start_time
    # print(f"Excution FPtree time:{execution_time} seconds")
