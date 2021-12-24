class classification:
    # Classify Base switching mutation & Base transversion mutation.

    def __init__(self, BSMhappens, BSMdepth, diffBSMhappens, diffBSMdepth, OTHERShappens, OTHERSdepth, diffOTHERShappens, diffOTHERSdepth, out):
        self.BSMhappens = BSMhappens
        self.BSMdepth = BSMdepth
        self.diffBSMhappens = diffBSMhappens
        self.diffBSMdepth = diffBSMdepth
        self.OTHERShappens = OTHERShappens
        self.OTHERSdepth = OTHERSdepth
        self.diffOTHERShappens = diffOTHERShappens
        self.diffOTHERSdepth = diffOTHERSdepth
        self.out = out
    
    # Classify Base switching mutation & Base transversion mutation.
    def classify(self, A, B, C, matched_group4, matched_group5,):
        base_switching_mutation = ['AG', 'GA', 'CT', 'TC']

        if len(A) == 1 and len(B) == 1 and len(C) == 1:
            # Base switching mutation. 
            if A == B and f'{B}{C}' in base_switching_mutation:
                self.BSMhappens.setdefault(f'{A}|{B}|{C}', 0)
                self.BSMhappens[f'{A}|{B}|{C}'] += int(matched_group4)
                self.BSMdepth.setdefault(f'{A}|{B}|{C}', 0)
                self.BSMdepth[f'{A}|{B}|{C}'] += int(matched_group5)
            
            elif A != B and f'{B}{C}' in base_switching_mutation:
                self.diffBSMhappens.setdefault(f'{A}|{B}|{C}', 0)
                self.diffBSMhappens[f'{A}|{B}|{C}'] += int(matched_group4)
                self.diffBSMdepth.setdefault(f'{A}|{B}|{C}', 0)
                self.diffBSMdepth[f'{A}|{B}|{C}'] += int(matched_group5)
            
            # Base transversion mutation.
            elif A == B and f'{B}{C}' not in base_switching_mutation:
                self.OTHERShappens.setdefault(f'{A}|{B}|{C}', 0)
                self.OTHERShappens[f'{A}|{B}|{C}'] += int(matched_group4)
                self.OTHERSdepth.setdefault(f'{A}|{B}|{C}', 0)
                self.OTHERSdepth[f'{A}|{B}|{C}'] += int(matched_group5)

            else:
                self.diffOTHERShappens.setdefault(f'{A}|{B}|{C}', 0)
                self.diffOTHERShappens[f'{A}|{B}|{C}'] += int(matched_group4)
                self.diffOTHERSdepth.setdefault(f'{A}|{B}|{C}', 0)
                self.diffOTHERSdepth[f'{A}|{B}|{C}'] += int(matched_group5)

        else:
            pass

        return self.BSMhappens, self.BSMdepth, self.diffBSMhappens, self.diffBSMdepth, self.OTHERShappens, self.OTHERSdepth, self.diffOTHERShappens, self.diffOTHERSdepth

    # Write file.
    def classificationFile(self, happens, depth, BSMornot, diffornot, file):
        import os
        totalhappens = 0
        for hv in happens.values():
            totalhappens += hv

        totaldepth = 0
        for dv in depth.values():
            totaldepth += dv

        with open(os.path.join(self.out, f'Base_switching_mutation&Base_transversion_mutation_{file}.txt'), 'a') as out:
            if BSMornot and diffornot:
                out.write('Base switching mutation(A != B)\n')
                for k, v in happens.items():
                    out.write(f'{k}: happens-{v} depth-{depth[k]} ratio-{v/depth[k]}\n')
                out.write(f'Total happens: {happens}\n')
                out.write(f'Total depth: {depth}\n')
                out.write(f'Total ratio: {totalhappens/totaldepth}\n\n')
            
            elif BSMornot and diffornot == False:
                out.write('Base switching mutation(A == B)\n')
                for k, v in happens.items():
                    out.write(f'{k}: happens-{v} depth-{depth[k]} ratio-{v/depth[k]}\n')
                out.write(f'Total happens: {happens}\n')
                out.write(f'Total depth: {depth}\n')
                out.write(f'Total ratio: {totalhappens/totaldepth}\n\n')
            
            elif BSMornot == False and diffornot:
                out.write('Base transversion mutation(A != B)\n')
                for k, v in happens.items():
                    out.write(f'{k}: happens-{v} depth-{depth[k]} ratio-{v/depth[k]}\n')
                out.write(f'Total happens: {happens}\n')
                out.write(f'Total depth: {depth}\n')
                out.write(f'Total ratio: {totalhappens/totaldepth}\n\n')

            else:
                out.write('Base transversion mutation(A == B)\n')
                for k, v in happens.items():
                    out.write(f'{k}: happens-{v} depth-{depth[k]} ratio-{v/depth[k]}\n')
                out.write(f'Total happens: {happens}\n')
                out.write(f'Total depth: {depth}\n')
                out.write(f'Total ratio: {totalhappens/totaldepth}\n\n')

# Test
if __name__ == '__main__':
    import sys, re, os
    from classification import *

    inputFolder = sys.argv[1]
    outputPath = sys.argv[2]

    Classify = classification()
    regex = re.compile(r'([ATCG])\|([ATCG])\|([ATCG])\s(\w*)\s.\s(\w*)')

    BSMhappens = {}
    BSMdepth = {}
    diffBSMhappens = {}
    diffBSMdepth = {}
    OTHERShappens = {}
    OTHERSdepth = {}
    diffOTHERShappens = {}
    diffOTHERSdepth = {}
    Classify = classification(BSMhappens, BSMdepth, diffBSMhappens, diffBSMdepth, OTHERShappens, OTHERSdepth, diffOTHERShappens, diffOTHERSdepth)

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

                    BSMhappens, BSMdepth, diffBSMhappens, diffBSMdepth, OTHERShappens, OTHERSdepth, diffOTHERShappens, diffOTHERSdepth = Classify.classify(A, B, C, matched.group(4), matched.group(5))

    print('Generating file...')    
    Classify.classificationFile(BSMhappens, BSMdepth, True, False, file)
    Classify.classificationFile(diffBSMhappens, diffBSMdepth, True, True, file)
    Classify.classificationFile(OTHERShappens, OTHERSdepth, False, False, file)
    Classify.classificationFile(diffOTHERShappens, diffOTHERSdepth, False, True, file)
    