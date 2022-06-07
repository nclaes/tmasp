'''
TMASP - Tsetlin Machine Architecture Search Paradigm
2022 Newcastle University

Weights and Biases Hyperparameter Search for Tsetlin Machines

    https://docs.wandb.ai/guides/sweeps/quickstart
    https://docs.wandb.ai/examples

    To use: 

    python3 w_b.py --C 50,200,50 --s 5,10,0.50 --T 10,15,0.50 --e 50,100,50

    What the above means: 

        --C 50 200 50   : go from 50 to 200 clauses in increments of 50
        --s 5 10 0.50   : go from 5 to 10 in s value in increments of 0.50
        --T 10 15 0.50  : go from 10 to 15 in T value in increments of 0.50
        --e 50 100 50   : go from 50 to 100 in epochs in increments of 50

    This script launches the sweep. 
    The sweep uses the hyp_search.py script.

'''
import subprocess
import argparse
import os

def process_args(arguments, hyperparameters):
    args_dict = dict(vars(arguments))
    for key, value in args_dict.items():
        dummy_array = []
        dummy_list = list(map(float, value.split(",")))
        i = dummy_list[0]
        while i < dummy_list[1]:
            dummy_array.append(i)
            i+= dummy_list[2]
        if (i >= dummy_list[1]):
            dummy_array.append(dummy_list[1])
        hyperparameters.append(dummy_array)
        

def create_yaml(hyps, run_name):
    hyper_params = ["clauses", "s_value", "T_value", "epochs"]
    f = open("hyp_search.yaml", "w")
    f.write("program: hyp_search.py\n")
    f.write("command: \n")
    f.write("  - ${env}\n")
    f.write("  - python3\n")
    f.write("  - ${program}\n")
    f.write("  - ${args}\n")
    f.write("method: grid\n")
    f.write("name: {0}\n".format(run_name))
    f.write("metric:\n")
    f.write("  goal: maximize\n")
    f.write("  name: acc\n")
    f.write("parameters:\n")
    param_counter = len(hyps)
    for i in range(len(hyper_params)):
        f.write("  " +hyper_params[i] + ": \n")
        f.write("    values: [")
        element = hyps[i]
        for j in range(len(element)):
            f.write(str(element[j]))
            if j < len(element)-1:
                f.write(", ")
            else:
                f.write("]\n")
    f.close()

# Warnings
print("If there are issues please consult the README")
print("Results are seen in real time through the  W&B link below:")

# Parse the arguments for the hyperparameter search
parser = argparse.ArgumentParser(description='Tsetlin Machine Hyperparameter Search Space')
parser.add_argument('--C', action='store', type=str, required=True, help='Enter clauses --C [start],[end],[inc]')
parser.add_argument('--s', action='store', type=str, required=True, help='Enter s parameter --s [start],[end],[inc]')
parser.add_argument('--T', action='store', type=str, required=True, help='Enter threshold (T) --T [start],[end],[inc]')
parser.add_argument('--e', action='store', type=str, required=True, help='Enter Epochs --e [start],[end],[inc]')
parser.add_argument('--run', action='store', type=str, required=True, help='Enter Name of W&B Run' )
args = parser.parse_args()

run_name = args.run 

ta_dir = run_name
print("Creating directory for storing TA files: ", ta_dir+ "_TMASP_TA_files")

ta_dir += "_TMASP_TA_files"
os.mkdir(ta_dir)


del args.run
# Process the user inputs into the approriate arrays
hyps = []
process_args(args, hyps)

# Process the user inputs and create the yaml file 
create_yaml(hyps, run_name)

# Write a dictionary to file. This is the start point
textfile = open("intial_setup.txt", "w")
#           C             s           T           e
setup = [hyps[0][0], hyps[1][0], hyps[2][0], hyps[3][0]]
for element in setup:
    textfile.write(str(element) + "\n")
textfile.write(run_name)
textfile.close()

# Run the sweep
with open('running_instructions.txt', 'w') as out:
    return_code = subprocess.call(["wandb" ,"sweep" ,"hyp_search.yaml"], stdout=out)


