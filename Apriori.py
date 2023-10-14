import argparse
from itertools import combinations
import csv
import time
def read_dataset(filename):
    dataset = []
    transactions = {}
    num_transaction = 0

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            #customer_id = int(parts[0])
            transaction_id = int(parts[1])
            item_id = int(parts[2])

            if transaction_id not in transactions:
                transactions[transaction_id] = []
                num_transaction += 1
            transactions[transaction_id].append(item_id)

    dataset = list(transactions.values())
    return dataset, num_transaction
    
def get_candidate_1_itemsets(dataset, num_transaction, min_sup):
    first_itemsets={}

    for transaction in dataset:
        for item_id in transaction:
            if item_id in first_itemsets:
                first_itemsets[item_id] += 1
            else:
                first_itemsets[item_id] = 1
    
    filter_candidate_1 = {}
    for item_id, support in first_itemsets.items():
        # test = support / num_transaction
        if support / num_transaction >= min_sup:
            filter_candidate_1[frozenset([item_id])] = support
    return filter_candidate_1 

def generate_candidate_k(frequent_itemsets, k, min_sup):
    candidate_k = set()
    for itemset1 in frequent_itemsets:
        for itemset2 in frequent_itemsets:
            if(len(itemset1.union(itemset2))) == k:
                candidate_k.add(itemset1.union(itemset2))
    return candidate_k

def filter_candidate_k(dataset, candidate_k, min_sup, num_transaction):
    candidate_support = {}
    for transaction in dataset:
        for itemset in candidate_k:
            if itemset.issubset(transaction):
                if itemset in candidate_support:
                    candidate_support[itemset] += 1
                else:
                    candidate_support[itemset] = 1
    filter_itemset ={}
    for itemset, support in candidate_support.items():
        if support / num_transaction >= min_sup:
            filter_itemset[itemset] = support
    return filter_itemset

def generate_association_rule(dataset, min_sup, min_conf, num_transaction):
    frequent_itemsets={}
    k = 1
    association_rules = []
    while True:
        if k == 1:
            candidate_k_itemsets = get_candidate_1_itemsets(dataset, num_transaction, min_sup)
        else:
            candidate_k_itemsets = generate_candidate_k(frequent_itemsets[k - 1], k, min_sup)

        if not candidate_k_itemsets:
            break
        if k > 1:
            candidate_k_itemsets = filter_candidate_k(dataset, candidate_k_itemsets, min_sup, num_transaction)

        frequent_itemsets[k] = candidate_k_itemsets
        k += 1
    
    for k, frequent_k_itemsets in frequent_itemsets.items():
        if k < 2:
            continue
        for itemset in frequent_k_itemsets:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequence = itemset - antecedent
                    support_antecedent = frequent_itemsets[len(antecedent)][antecedent]/ num_transaction
                    support_consequence = frequent_itemsets[len(consequence)][consequence] / num_transaction
                    support_itemset = frequent_itemsets[k][itemset] / num_transaction
                    confidence = support_itemset / support_antecedent
                    lift = support_itemset / (support_antecedent * support_consequence)
                    if confidence >= min_conf:
                        association_rules.append((antecedent, consequence, support_itemset, confidence, lift))

    return association_rules
    
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


if __name__ == "__main__":
    test_args={
        "dataset": "set10.txt",
        "min_sup": 0.05,
        "min_conf": 0.05
    }
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
    dataset, num_transaction = read_dataset(dataset_path)
    associaiton_rules = generate_association_rule(dataset, args.min_sup, args.min_conf, num_transaction)
    output_file = f'outputs/{args.dataset.replace(".txt", "-apriori")}-{args.min_sup}-{args.min_conf}.csv'
    write_to_csv(associaiton_rules, output_file)

    end_time = time.time()
    execution_time = end_time - start_time
    # print(f"Excution Apriori time:{execution_time} seconds")



    



