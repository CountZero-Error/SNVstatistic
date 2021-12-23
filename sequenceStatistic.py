# sequenceStatistic.py - statistics of different type base-pairs that required by user.
# Usage: python abs/sequenceStatistic.py <input folder path> <output file path> <conditions file path>

import re, os, argparse, time
from sequenceStatisticTools import *
from drawChart import *
from classification import *

parse = argparse.ArgumentParser(description='This program allows to use at most 10 conditions only!')
parse.add_argument('-I', '--input_folder_path', required=True, type=str, help='Enter the path of input file.')
parse.add_argument('-O', '--output_folder_path', required=True, type=str, help='Enter the path of output file.')
parse.add_argument('-conditions', '--conditions_file_path', required=True, type=str, help='Enter the path of file contains conditions you need.')
parse.add_argument('-draw', '--draw_bar_chart', type=str, help='Enter the condition that you want to draw a bar chart. If you want to draw bar chart for multi conditions, write all of them in form A/B/C.')
args = parse.parse_args()

inputFolder = args.input_folder_path
output = args.output_folder_path
conditionsFile = args.conditions_file_path
drawBarChart = args.draw_bar_chart
regex = re.compile(r'([ATCG])\|([ATCG])\|([ATCG])\s(\w*)\s.\s(\w*)')
statistics = sequenceStatisticTools()
Classify = classification()

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
# Base_switching_mutation&Base_transversion_mutation.txt.
AChappens = {}
ACdepth = {}
OTHERShappens = {}
OTHERSdepth = {}

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
            
            AChappens, ACdepth, OTHERShappens, OTHERSdepth = Classify.classify(AChappens, ACdepth, OTHERShappens, OTHERSdepth, A, B, C, matched.group(4), matched.group(5))
        
    # Finish.
    print('Finish.\n\n\n')
    time.sleep(1)
    print('Writting to file...')

    # Base_switching_mutation&Base_transversion_mutation.txt.
    Classify.classificationFile(AChappens, ACdepth, OTHERShappens, OTHERSdepth, output)
    # Results.
    fileName = os.path.basename(file)
    outputFile = os.path.join(output, f'{fileName[:-4]}_statistic.txt')
    with open(outputFile, 'w') as out:
        out.write(os.path.basename(file))
        out.write('\nA|B|C\n')

        # Determine which conditions need to draw bar chart.
        if drawBarChart == None:
            Draw = False
        else:
            chartRequired = drawBarChart
            Draw = True

        for i in range(len(conditionsName)):
            if conditionsName[i] == 'AeB':
                statistics.writeFile(out, dicts[i], 'A->C', outputFile)
                if Draw:
                    conditionsList = chartRequired.split('/')
                    if 'A==B' in conditionsList:
                        chart = drawChart()
                        chart.drawing(dicts[i], os.path.basename(file), output, 'A->C', conditionsName[i])
                time.sleep(1)
                
            else:
                statistics.writeFile(out, dicts[i], conditions[i], outputFile)
                if Draw:
                    conditionsList = chartRequired.split('/')
                    if conditions[i].replace(' ','') in conditionsList:
                        chart = drawChart()
                        chart.drawing(dicts[i], os.path.basename(file), output, conditions[i], conditionsName[i])
                time.sleep(1)

        # Unmatched
        out.write(f'\nUnmatched: \n')
        for elm in anomaly:
            out.write(f'{elm}')
