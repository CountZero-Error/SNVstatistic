# sequenceStatistic.py - statistics of different type base-pairs that required by user.
# Usage: python abs/sequenceStatistic.py <input folder path> <output file path> <conditions file path>

import re, os, argparse, time
from sequenceStatisticTools import *
from drawChart import *
from classification import *

parse = argparse.ArgumentParser()
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
chart = drawChart()

# Base_switching_mutation&Base_transversion_mutation.txt.
BSMhappens = {}
BSMdepth = {}
diffBSMhappens = {}
diffBSMdepth = {}
OTHERShappens = {}
OTHERSdepth = {}
diffOTHERShappens = {}
diffOTHERSdepth = {}
try:
    os.mkdir(os.path.join(output, 'BSM&BTM'))
except FileExistsError:
    pass
Classify = classification(BSMhappens, BSMdepth, diffBSMhappens, diffBSMdepth, OTHERShappens, OTHERSdepth, diffOTHERShappens, diffOTHERSdepth, os.path.join(output, 'BSM&BTM'))

# Read from conditions file(preprocessing).
conditions, conditionsName = statistics.perprocessing(conditionsFile)

# Create dictionaries.
dicts = []
for i in range(len(conditions)):
    dicti = {}
    dicts.append(dicti)
    
# Anomaly list.
anomaly = []

# Statistic
for file in os.listdir(inputFolder):
    totalHappens = 0
    totalDepth = 0    
    with open(os.path.join(inputFolder, file)) as filo:
        for line in filo:
            print(f'Processing line...{line}')
            matched = regex.search(line)
            
            # A|B|C
            if matched != None:

                A = matched.group(1)
                B = matched.group(2)
                C = matched.group(3)

                totalHappens += int(matched.group(4))
                totalDepth += int(matched.group(5))
            
            for i in range(len(conditions)):
                if matched != None and eval(conditions[i]):
                    if conditions[i] == 'A == B':
                        key = f'{A}→{C}'
                    else:
                        key = f'{A}|{B}|{C}'
                    statistics.statistic(dicts[i], key, matched.group(4), matched.group(5))

                elif matched == None:
                    anomaly.append(line)
            
            if matched != None:
                BSMhappens, BSMdepth, diffBSMhappens, diffBSMdepth, OTHERShappens, OTHERSdepth, diffOTHERShappens, diffOTHERSdepth = Classify.classify(A, B, C, matched.group(4), matched.group(5))
        
    # Finish.
    print('Finish.\n\n\n')
    time.sleep(1)
    print('Writting to file...')

    # Base_switching_mutation&Base_transversion_mutation.txt.
    Classify.classificationFile(BSMhappens, BSMdepth, True, False, file)
    chart.drawBSMandBTM(BSMhappens, BSMdepth, True, file, os.path.join(output, 'BSM&BTM'))
    Classify.classificationFile(diffBSMhappens, diffBSMdepth, True, True, file)
    Classify.classificationFile(OTHERShappens, OTHERSdepth, False, False, file)
    chart.drawBSMandBTM(OTHERShappens, OTHERSdepth, False, file, os.path.join(output, 'BSM&BTM'))
    Classify.classificationFile(diffOTHERShappens, diffOTHERSdepth, False, True, file)
    chart.summaryBSMandBTM(BSMhappens, BSMdepth, OTHERShappens, OTHERSdepth, file, os.path.join(output, 'BSM&BTM'))

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
                statistics.writeFile(out, dicts[i], 'A→C', outputFile)
                if Draw:
                    conditionsList = chartRequired.split('/')
                    if 'A==B' in conditionsList:
                        chart.drawing(dicts[i], os.path.basename(file), output, 'A→C', conditionsName[i])
                time.sleep(1)
                
            else:
                statistics.writeFile(out, dicts[i], conditions[i], outputFile)
                if Draw:
                    conditionsList = chartRequired.split('/')
                    if conditions[i].replace(' ','') in conditionsList:
                        chart.drawing(dicts[i], os.path.basename(file), output, conditions[i], conditionsName[i])
                time.sleep(1)
        
        # Summary.
        out.write('\nSummary\n')
        out.write(f'Total happens: {totalHappens}\n')
        out.write(f'Total depth: {totalDepth}\n')

        # Unmatched
        out.write(f'\nUnmatched: \n')
        for elm in anomaly:
            out.write(f'{elm}')
