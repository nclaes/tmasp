'''
TMASP - Tsetlin Machine Architecture Search Paradigm
2022 Newcastle University
'''
import wandb
import re
import os
import sys
import subprocess
import sqlite3 as sqlite
import shutil
# Create a database that can be accessed later


conn = sqlite.connect("hyperparamter_serarch.db")

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS TM_SETTINGS(

        clauses     real, 
        s           real,
        T           real, 
        epochs      real,
        includes    real, 
        accuracy    real,
        ta_file     text    
        )""")

conn.commit()


# Weights and Biases Account 
wandb.init(project='TM_include_encoding_hyp', entity='tousif')

# Initial Configuration
with open('intial_setup.txt') as f:
    setup= [line.rstrip() for line in f]
config={
    "clauses" : setup[0],
    "s_value": setup[1],
    "T_value" : setup[2],
    "epochs": setup[3]
}
config = wandb.config

run_name = setup[4]

# Change the header file:
KEYWORDS=["S","THRESHOLD","CLAUSES", "EPOCHS"]
VALS=[config["s_value"],config["T_value"], config["clauses"], config["epochs"]] 
ta_dir = run_name
ta_dir += "_TMASP_TA_files/"


with open('UserSetup2.h','r') as f1, open('UserSetup.h','w') as f2:
    for line in f1:
        for i in range(len(KEYWORDS)):
            line = line.replace("#define " + KEYWORDS[i], "#define " + KEYWORDS[i] + " " + str(VALS[i]))
        f2.write(line)

# Now we run the Makefile
process = subprocess.Popen("make", shell=True, stdout=subprocess.PIPE)
process.wait()

# Now we run the code 
f = open("result.txt", "w")
process = subprocess.Popen("./hyp_search", shell=True, stdout=f)
process.wait()
acc = 0.0
inc = 0
RESULT_KEYWORDS = ["Accuracy","Includes"]
with open("result.txt") as result_file:
    for line in result_file:
        # find the keyword and get its value
        if line.startswith(RESULT_KEYWORDS[0]):
            s=line.split()
            acc = float(s[1])
        if line.startswith(RESULT_KEYWORDS[1]):
            s=line.split()
            inc = int(s[1])
print('-------------------------------------')
print('Accuracy = ', acc)
print('Includes = ', inc)
print('-------------------------------------')
# Log metrics over time to visualize performance
metrics = {"Accuracy": acc, "Includes": inc }

ta_file_str = run_name +"_TA_FILE_C" + str(config["clauses"]) +"_S" + str(int(config["s_value"])) + "_T"+ str(int(config["T_value"])) + "_E"+ str(config["epochs"]) + ".txt"
s = str(float(config["s_value"]))
T = str(float(config["T_value"]))
s_d=  s.split(".")[1]
t_d = T.split(".")[1]
ta_file_str_new = run_name +"_TA_FILE_C" + str(config["clauses"]) +"_S" + str(int(config["s_value"])) + "_"+ str(int(s_d)) + "_T"+ str(int(config["T_value"])) + "_" + str(int(t_d)) + "_E"+ str(config["epochs"]) + ".txt"
os.rename(ta_file_str, ta_file_str_new)
ta_file_str = ta_file_str_new

# Move the fies to the directory that was created
shutil.move(ta_file_str, ta_dir+ta_file_str)

c.execute("INSERT INTO TM_SETTINGS (clauses, s, T, epochs, includes, accuracy, ta_file) VALUES (?, ?, ?, ?, ?, ?,?)",
            (config["clauses"], config["s_value"], config["T_value"], config["epochs"], inc, acc, ta_file_str))

conn.commit()
wandb.log(metrics)

conn.close()


