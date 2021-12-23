class classification:
    def __init__(self) -> None:
        pass
    
    # Classify Base switching mutation & Base transversion mutation.
    def classify(self, AChappens, ACdepth, OTHERShappens, OTHERSdepth, A, B, C, matched_group4, matched_group5):
        base_switching_mutation = ['AG', 'GA', 'CT', 'TC']

        if len(B) == 1: 
            if f'{A}{C}' in base_switching_mutation:
                AChappens.setdefault(f'{A}|{B}|{C}', 0)
                AChappens[f'{A}|{B}|{C}'] += int(matched_group4)
                ACdepth.setdefault(f'{A}|{B}|{C}', 0)
                ACdepth[f'{A}|{B}|{C}'] += int(matched_group5)
            
            else:
                OTHERShappens.setdefault(f'{A}|{B}|{C}', 0)
                OTHERShappens[f'{A}|{B}|{C}'] += int(matched_group4)
                OTHERSdepth.setdefault(f'{A}|{B}|{C}', 0)
                OTHERSdepth[f'{A}|{B}|{C}'] += int(matched_group5)
        else:
            pass
        return AChappens, ACdepth, OTHERShappens, OTHERSdepth

    # Write file.
    def classificationFile(self, AChappens, ACdepth, OTHERShappens, OTHERSdepth, output):
        import os
        totalAChappens = 0
        for BSMhv in AChappens.values():
            totalAChappens += BSMhv

        totalACdepth = 0
        for BSMdv in ACdepth.values():
            totalACdepth += BSMdv
        
        totalOTHERShappens = 0
        for BTMhv in OTHERShappens.values():
            totalOTHERShappens += BTMhv
        
        totalOTHERSdepth = 0
        for BTMdv in OTHERSdepth.values():
            totalOTHERSdepth += BTMdv

        with open(os.path.join(output, 'Base_switching_mutation&Base_transversion_mutation.txt'), 'w') as out:
            out.write('Base switching mutation\n')
            for k, v in AChappens.items():
                out.write(f'{k}: happens-{v} depth-{ACdepth[k]} ratio-{v/ACdepth[k]}\n')
            out.write(f'Total happens: {totalAChappens}\n')
            out.write(f'Total depth: {totalACdepth}\n')
            out.write(f'Total ratio: {totalAChappens/totalACdepth}\n\n')

            out.write('Base transversion mutation.txt\n')
            for k, v in OTHERShappens.items():
                out.write(f'{k}: happens-{v} depth-{OTHERSdepth[k]} ratio-{v/OTHERSdepth[k]}\n')
            out.write(f'Total happens: {totalOTHERShappens}\n')
            out.write(f'Total depth: {totalOTHERSdepth}\n')
            out.write(f'Total ratio: {totalOTHERShappens/totalOTHERSdepth}\n\n')

# Test
if __name__ == '__main__':
    import sys, re, os
    from classification import *

    inputFolder = sys.argv[1]
    outputPath = sys.argv[2]

    Classify = classification()
    regex = re.compile(r'([ATCG])\|([ATCG])\|([ATCG])\s(\w*)\s.\s(\w*)')

    AChappens = {}
    ACdepth = {}
    OTHERShappens = {}
    OTHERSdepth = {}

    files = os.listdir(inputFolder)
    for file in files:
        print(f'Processing file - {file}')
        with open(os.path.join(inputFolder, file)) as filo:
            for line in filo:
                print(f'  Processing line - {line}')
                matched = regex.search(line)
                
                # A|B|C
                if matched != None:
                    A = matched.group(1)
                    B = matched.group(2)
                    C = matched.group(3)

                    AChappens, ACdepth, OTHERShappens, OTHERSdepth = Classify.classify(AChappens, ACdepth, OTHERShappens, OTHERSdepth, A, B, C, matched.group(4), matched.group(5))

    print('Generating file...')    
    Classify.classificationFile(AChappens, ACdepth, OTHERShappens, OTHERSdepth, outputPath)
