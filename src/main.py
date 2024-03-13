import subprocess
import argparse
import time

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type = str, required = True)
parser.add_argument("--min_sup", type = float, required = True)
parser.add_argument("--min_conf", type = float, required = True)
args = parser.parse_args()

dataset = str(args.dataset)
min_sup = str(args.min_sup)
min_conf = str(args.min_conf)

subprocess.call(["python3", "./Apriori.py", "--dataset", dataset, "--min_sup", min_sup, "--min_conf", min_conf])
subprocess.call(["python3", "./fp_growth.py", "--dataset", dataset, "--min_sup", min_sup, "--min_conf", min_conf])

end_time = time.time()
execution_time = end_time - start_time
# print(f"Excution total time:{execution_time} seconds")
