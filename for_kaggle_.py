from Apriori import generate_association_rule
import time
import csv
def read_dataset(filename):
    counter = 1
    item_to_number = {}
    relation_table = {}

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            item_description = parts[2]

            if item_description not in item_to_number:
                item_to_number[item_description] = counter
                counter += 1
                
            transaction_id = parts[0]                    
            if transaction_id not in relation_table:
                relation_table[transaction_id] = []
            relation_table[transaction_id].append(item_to_number[item_description])
        dataset = list(relation_table.values())
    return dataset, len(dataset), item_to_number

def write_to_csv(association_rules, output_file, item_to_number):
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['antecedent', 'consequent', 'support', 'confidence', 'lift'])
        for rule in association_rules:
            antecedent = "[{}]".format(', '.join([f"'{list(item_to_number.keys())[list(item_to_number.values()).index(item)]}'" for item in rule[0]]))
            consequent = "[{}]".format(', '.join([f"'{list(item_to_number.keys())[list(item_to_number.values()).index(item)]}'" for item in rule[1]]))
            support = round(rule[2], 2)
            confidence = round(rule[3], 2)
            lift = round(rule[4], 2)
            csv_writer.writerow([antecedent, consequent, support, confidence, lift])


if __name__ == "__main__":
    start_time = time.time()

    dataset_path = f'./inputs/kaggle.txt'
    dataset, num_transaction, item_to_number = read_dataset(dataset_path)
    min_sup = 0.2
    min_conf = 0.05
    associaiton_rules = generate_association_rule(dataset, min_sup, min_conf, num_transaction)
    output_file = f'outputs/kaggle-apriori-{min_sup}-{min_conf}.csv'
    write_to_csv(associaiton_rules, output_file, item_to_number)

    end_time = time.time()
    execution_time = end_time - start_time
    # print(f"Excution Apriori time:{execution_time} seconds")
    
