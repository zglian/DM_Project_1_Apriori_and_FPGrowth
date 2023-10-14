import argparse
from collections import defaultdict
import csv
import time
from itertools import combinations

test_args = {
    "dataset": "example.txt",
    "min_sup": 0.222222,
    "min_conf": 0
}

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default=test_args["dataset"])
parser.add_argument("--min_sup", type=float, default=test_args["min_sup"])
parser.add_argument("--min_conf", type=float, default=test_args["min_conf"])
args = parser.parse_args()

class FPTreeNode:
    def __init__(self, item, count, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.node_link = None

def read_dataset(filename):
    dataset = []
    transactions = defaultdict(list)

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            transaction_id = int(parts[1])
            item_id = int(parts[2])
            transactions[transaction_id].append(item_id)

    dataset = list(transactions.values())
    return dataset

def fp_growth(dataset, min_sup, min_conf):
    def build_tree(dataset, min_sup):
        header_table = {}
        for transaction in dataset:
            for item in transaction:
                if item in header_table:
                    header_table[item][0] += 1
                else:
                    header_table[item] = [1, None]

        for item, (count, _) in list(header_table.items()):
            if count / 9 < min_sup:
                del header_table[item]

        header_table = dict(sorted(header_table.items(), key=lambda x: (-x[1][0], x[0])))

        root = FPTreeNode(None, None)

        for transaction in dataset:
            filtered_transaction = []
            for item in transaction:
                if item in header_table and header_table[item][0] >= min_sup:
                    filtered_transaction.append(item)

            sorted_items = sorted(filtered_transaction, key=lambda x: (header_table[x][0], x), reverse=True)
            current_node = root

            for item in sorted_items:
                if item in current_node.children:
                    current_node.children[item].count += 1
                else:
                    new_node = FPTreeNode(item, 1, current_node)
                    current_node.children[item] = new_node
                    update_node_link(item, new_node, header_table)
                current_node = current_node.children[item]
        
        return root, header_table

    def update_node_link(item, node, header_table):
        if item not in header_table:
            return
        last_node = header_table[item][1]
        if last_node is None:
            header_table[item][1] = node
        else:
            while last_node.node_link is not None:
                last_node = last_node.node_link
            last_node.node_link = node

    def ascendTree(node, prefix_path):
        if node.parent is not None:
            prefix_path.append(node.item)
            ascendTree(node.parent, prefix_path)
    
    def find_prefix_path(node):
        condPats = {}
        while node is not None:
            prefix_path = []
            ascendTree(node, prefix_path)
            if len(prefix_path) > 1:
                condPats[frozenset(prefix_path[1:])] = node.count
            node = node.node_link
        return condPats

    def find_frequent_itemsets(frequent_itemsets):
        for item, (count, node) in reversed(list(header_table.items())):
            newFreqSet = []
            newFreqSet.append(item)
            #print('new frequent=', newFreqSet, prefix)   #????
            frequent_itemsets.append((newFreqSet, count))
            condPathBases = find_prefix_path(node)
            myroot, mytable = build_tree(condPathBases, min_sup)
            if mytable is not None:
                mine_frequent_itemsets(myroot, mytable, newFreqSet, frequent_itemsets, count)

    # def mine_frequent_itemsets(root, header_table, min_sup, prefix, frequent_itemsets):
    #     frequent_itemsets = []
    #     for item, (count, node) in list(header_table.items()):
    #         find_frequent_itemsets(node, min_sup, [], frequent_itemsets)
    #     return frequent_itemsets
    def mine_frequent_itemsets(root, header_table, newFreqSet, frequent_itemsets, count):
    # Iterate over the header table in reverse order
        prefix = []
        # for  in root.children:
        #     print(test.item)
        #     print(test.count)
        root = root.children[2]
        if root.children is None:
            return
        for item, node in root:
            record(root, prefix, frequent_itemsets, count)

    def record(root, prefix, frequent_itemsets, count):
        if(root.children) is None:
            return (root.item)
        for item, node in root.children.item():
            frequent_itemsets.append((prefix + record(node, prefix, frequent_itemsets, count), count))


    def mine_rules(header_table, min_conf):
        frequent_itemsets = []
        find_frequent_itemsets(frequent_itemsets)
        
        rules = []
        #filter_frequent_itemset = []

        # for itemset, count in frequent_itemsets:
        #     if len(itemset) <= 1:
        #         continue
        #     for _itemset, _count in frequent_itemsets:
        #         if set(itemset).issubset(_itemset):
        #             count += 1
        #     count -= 1
        #     filter_frequent_itemset.append((itemset, count))

        for itemset, count in frequent_itemsets:
            if len(itemset) <= 1:
                continue
            if count / len(dataset) < min_sup:
                continue
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequence = frozenset(item for item in itemset if item not in antecedent)
                    support_antecedent = calculate_support(antecedent, dataset)
                    support_consequence = calculate_support(consequence, dataset)
                    support_itemset = count / len(dataset)
                    confidence = support_itemset / support_antecedent
                    lift = support_itemset / (support_antecedent * support_consequence)
                    if confidence >= min_conf:
                        rules.append((antecedent, consequence, support_itemset, confidence, lift))
        return rules
    



    def calculate_support(itemset, dataset):
    # Calculate the support count for an itemset
        support_count = 0
        for transaction in dataset:
            if itemset.issubset(transaction):
                support_count += 1
        return support_count / len(dataset)

    root, header_table = build_tree(dataset, min_sup)
    rules = mine_rules(header_table, min_conf)
    return rules

def write_to_csv(rules, output_file):
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['antecedent', 'consequent', 'support', 'confidence', 'lift'])
        for rule in rules:
            antecedent = f"[{', '.join(map(str, rule[0]))}]"
            consequent = f"[{', '.join(map(str, rule[1]))}]"
            support = round(rule[2], 2)
            confidence = round(rule[3], 2)
            lift = round(rule[4], 2)
            csv_writer.writerow([antecedent, consequent, support, confidence, lift])

if __name__ == "__main__":
    start_time = time.time()

    dataset_path = f'./inputs/{args.dataset}'
    dataset = read_dataset(dataset_path)
    association_rules = fp_growth(dataset, args.min_sup, args.min_conf)
    output_file = f'outputs/{args.dataset.replace(".txt", "-fp-tree")}-{args.min_sup}-{args.min_conf}.csv'
    write_to_csv(association_rules, output_file)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
