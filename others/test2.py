'''
# import argparse
# import csv
# import time
# from collections import defaultdict

# test_args = {
#     "dataset": "test.txt",
#     "min_sup": 0.222222,
#     "min_conf": 0
# }

# parser = argparse.ArgumentParser()
# parser.add_argument("--dataset", type=str, default=test_args["dataset"])
# parser.add_argument("--min_sup", type=float, default=test_args["min_sup"])
# parser.add_argument("--min_conf", type=float, default=test_args["min_conf"])
# args = parser.parse_args()

# def read_dataset(filename):
#     dataset = []
#     with open(filename, "r") as file:
#         for line in file:
#             items = list(map(int, line.strip().split()))
#             dataset.append(items)
#     return dataset

# def find_frequent_items(dataset, min_sup):
#     item_counts = defaultdict(int)
#     for transaction in dataset:
#         for item in transaction:
#             item_counts[item] += 1

#     frequent_items = {item: support for item, support in item_counts.items() if support / len(dataset) >= min_sup}
#     return frequent_items

# class FPNode:
#     def __init__(self, item, count, parent):
#         self.item = item
#         self.count = count
#         self.parent = parent
#         self.children = {}
#         self.next = None

# def build_fptree(dataset, min_sup):
#     header_table = find_frequent_items(dataset, min_sup)
#     sorted_items = sorted(header_table.items(), key=lambda x: (-x[1], x[0]))
#     ordered_items = [item[0] for item in sorted_items]
#     root = FPNode(None, 0, None)
#     tree = {}

#     for transaction in dataset:
#         transaction = [item for item in transaction if item in ordered_items]
#         current = root

#         for item in transaction:
#             if item in current.children:
#                 current.children[item].count += 1
#             else:
#                 current.children[item] = FPNode(item, 1, current)

#                 if item in tree:
#                     tree[item].next = current.children[item]
#                 else:
#                     tree[item] = current.children[item]

#             current = current.children[item]

#     return root, tree

# def mine_fptree(header_table, prefix, min_sup, association_rules):
#     for item in header_table:  # Iterate over keys (items) in header_table
#         count = header_table[item]
#         if count >= min_sup:
#             new_prefix = prefix + [item]
#             association_rules.append((new_prefix, [item], count))

#             conditional_base = []
#             node = header_table[item].next

#             while node:
#                 conditional_path = []
#                 count = node.count
#                 current = node.parent

#                 while current.item is not None:
#                     conditional_path.insert(0, current.item)
#                     current = current.parent

#                 conditional_base.extend([conditional_path] * count)
#                 node = node.next

#             conditional_tree, conditional_header_table = build_fptree(conditional_base, min_sup)

#             if conditional_header_table:
#                 mine_fptree(conditional_header_table, new_prefix, min_sup, association_rules)

# def generate_association_rules(fptree, min_conf):
#     association_rules = []
#     mine_fptree(fptree, [], min_conf, association_rules)
#     return association_rules

# def write_to_csv(association_rules, output_file):
#     with open(output_file, 'w', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(['antecedent', 'consequent', 'support', 'confidence'])
#         for rule in association_rules:
#             antecedent = f"[{', '.join(map(str, rule[0]))}]"
#             consequent = f"[{', '.join(map(str, rule[1]))}]"
#             support = rule[2]
#             confidence = rule[3]
#             csv_writer.writerow([antecedent, consequent, support, confidence])

# if __name__ == "__main__":
#     start_time = time.time()
#     dataset_path = f'./inputs/{args.dataset}'
#     dataset = read_dataset(dataset_path)
#     fptree, _ = build_fptree(dataset, args.min_sup)
#     association_rules = generate_association_rules(fptree, args.min_conf)
#     output_file = f'outputs/{args.dataset.replace(".txt", "-fp-growth")}-{args.min_sup}-{args.min_conf}.csv'
#     write_to_csv(association_rules, output_file)
#     end_time = time.time()
#     execution_time = end_time - start_time
#     print(f"Execution time: {execution_time} seconds")

'''

import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type = str, required = True)
parser.add_argument("--min_sup", type = float, required = True)
parser.add_argument("--min_conf", type = float, required = True)
# parser.add_argument("--dataset", type=str, default=test_args["dataset"])
# parser.add_argument("--min_sup", type=float, default=test_args["min_sup"])
# parser.add_argument("--min_conf", type=float, default=test_args["min_conf"])
args = parser.parse_args()
dataset = str(args.dataset)
min_sup = str(args.min_sup)
min_conf = str(args.min_conf)

subprocess.call(["python3", "./Apriori.py", "--dataset", dataset, "--min_sup", min_sup, "--min_conf", min_conf])
subprocess.call(["python3", "./b.py"])

# Execute script2.py with its arguments
# subprocess.call(["python", f'./b.py'])

