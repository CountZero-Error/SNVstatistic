class sequenceStatisticTools():

    def __init__(self) -> None:
        pass

    # Count the total depth.
    def totalNumber(self, dict):
        Sum = 0
        for v in dict.values():
            Sum += v['depth']
        return Sum

    # Print the infomation of each type base-pairs.(<type>: <total number>   <ratio>)
    def dictPrint(self, dict, out):
        for k, v in dict.items():
            try:
                number = v['number']
                rate = v['happens']/v['depth']
                out.write(f'{k}: {number}   ratio: {rate}\n')
            except ZeroDivisionError:
                out.write(f'{k}: {number}   ratio: 0\n')

    # Print the sum of all types and its ratio.
    def total(self, dict, out):
        number = 0
        happens = 0
        depth = 0
        for v in dict.values():
            number += v['number']
            happens += v['happens']
            depth += v['depth']
        out.write(f'Total number: {number}\n')
        try:
            out.write(f'Ratio = {happens/depth}\n')
        except ZeroDivisionError:
            out.write('Ratio = 0\n')

    # Process file to different types statistic.
    def statistic(self, dict, key, happens, depth):
        dict.setdefault(key, {'number': 0, 'happens': 0, 'depth': 0})
        dict[key]['number'] += 1
        dict[key]['happens'] += int(happens)
        dict[key]['depth'] += int(depth)

    def writeFile(self, out, dict, dictName, fileName):
        print(f'Writting to {fileName}...')
        out.write(f'\nStatistic {dictName}:\n')
        self.dictPrint(dict, out)
        self.total(dict, out)
    
    def perprocessing(self, conditionsFile):
        import sys

        with open(conditionsFile) as condition:
            conditionsName = []
            conditions = []

            for line in condition:
                if line.startswith('#'):
                    pass
                elif line == '\n':
                    pass
                else:
                    tmp = line
                    # Delete space.
                    tmp = tmp.replace(' ', '')
                    # Replace '==' to 'e'.
                    tmp = tmp.replace('==', 'e')
                    # Replace '!=' to 'n'.
                    tmp = tmp.replace('!=', 'n')
                    # If more than two conditions.
                    if len(tmp) >= 9: 
                        tmp = tmp.replace('and', '')
                        # AeCAnB -> AeCnB or CeAAnB -> CeAnB.
                        if tmp[0] == tmp[3] or tmp[2] == tmp[3]:
                            tmp = list(tmp)
                            tmp[3] = ''
                            tmp = ''.join(tmp)
                        # AeCBnA -> AeCnB or CeABnA -> CeAnB.
                        elif tmp[0] == tmp[5] or tmp[2] == tmp[5]:
                            tmp = list(tmp)
                            tmp[5] = ''
                            tmp.append(tmp[3])
                            tmp[3] = ''
                            tmp = ''.join(tmp)
                    
                    # Delete all '\n'.
                    tmp = tmp.replace('\n', '')

                    # Store tmp and line
                    conditionsName.append(tmp)
                    conditions.append(line.replace('\n',''))

                    if len(conditions) > 10:
                        print('This program allows to use at most 10 conditions only!')
                        sys.exit()

        return conditions, conditionsName
