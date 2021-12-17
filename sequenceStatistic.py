# sequenceStatistic.py - statistics of different type base-pairs that required by user.
# Usage: python abs/sequenceStatistic.py <input folder path> <output file path> <conditions file path>
# Last update: 2021-12-15 18:00:59

import re, os, argparse
from V1.sequenceStatisticTools import *
from V1.drawChart import *

parse = argparse.ArgumentParser(description='This program allows to use at most 10 conditions only!')
parse.add_argument('-I', '--input_folder_path', required=True, type=str, help='Enter the path of input file.')
parse.add_argument('-O', '--output_file_path', required=True, type=str, help='Enter the path of output file.')
parse.add_argument('-conditions', '--conditions_file_path', required=True, type=str, help='Enter the path of file contains conditions you need.')
args = parse.parse_args()

inputFolder = args.input_folder_path
output = args.output_file_path
conditionsFile = args.conditions_file_path
regex = re.compile(r'([ATCG])\|([ATCG])\|([ATCG])\s(\w*)\s.\s(\w*)')
statistics = sequenceStatisticTools()

# Create 10 dictionaries.
dict1 = {}
dict2 = {}
dict3 = {}
dict4 = {}
dict5 = {}
dict6 = {}
dict7 = {}
dict8 = {}
dict9 = {}
dict10 = {}
# Store dictionaries in a list.
dicts = [dict1, dict2, dict3, dict4, dict5, dict6, dict7, dict8, dict9, dict10]
# Anomaly list.
anomaly = []

# Read from conditions file(preprocessing).
conditions, conditionsName = statistics.perprocessing(conditionsFile)

# Statistic
for file in os.listdir(inputFolder):
    with open(os.path.join(inputFolder, file)) as filo:
        for line in filo:
            print(f'Processing line...{line}')
            matched = regex.search(line)
            
            # A|B|C
            if matched != None:
                A = matched.group(1)
                B = matched.group(2)
                C = matched.group(3)
            
            for i in range(len(conditions)):
                if matched != None and eval(conditions[i]):
                    if conditions[i] == 'A == B':
                        key = f'{A}->{C}'
                    else:
                        key = f'{A}|{B}|{C}'
                    statistics.statistic(dicts[i], key, matched.group(4), matched.group(5))

                elif matched == None:
                    anomaly.append(line)
        
    # Finish.
    print('Done.\n\n\n')

    # Results.
    with open(os.path.join(output, f'{os.path.basename(file)}_statistic.txt'), 'w') as out:
        out.write(os.path.basename(file))
        out.write('\nA|B|C\n')

        for i in range(len(conditionsName)):
            if conditionsName[i] == 'AeB':
                statistics.writeFile(out, dicts[i], 'A->C')
                chart = drawChart()
                chart.drawing(dicts[i], os.path.basename(file), output)
            else:
                statistics.writeFile(out, dicts[i], conditions[i])

        # Unmatched
        out.write(f'\nUnmatched: \n')
        for elm in anomaly:
            out.write(f'{elm}')
