from matplotlib.pyplot import figure

class drawChart():

    def __init__(self) -> None:
        pass

    # Chart of ratio.
    def drawing(self, dict, title, outputPath, condition, fileName):
        import matplotlib.pyplot as plt
        import os, time

        nameList = []
        ratioList = []

        # Prepare data for chart.
        print('Processing data...')
        for key in dict.keys():
            top = dict[key]['happens']
            bottom = dict[key]['depth']
            
            nameList.append(key)
            ratioList.append(top/bottom)
        
        time.sleep(1)
        
        # Draw chart.
        print(f'Drawing Chart <{condition}>...')
        plt.figure()
        plt.bar(x=nameList, height=ratioList, width=0.5)
        plt.xticks(rotation=45)
        plt.ylabel('Ratio', fontsize=10)
        plt.title(f'{title}_{fileName}', fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(outputPath, f'{title[:-4]}_{fileName}.png'))
        time.sleep(1)

        # Finish.
        print('Done')

    # Sperate chart.
    # Chart of either Base switching mutation or Base transversion mutation.
    def drawBSMandBTM(self, happens, depth, isBSM, fileName, outputPath):
        import matplotlib.pyplot as plt
        import os, time

        nameList = []
        ratioList = []

        # Prepare data for chart.
        print('Processing data...')
        for k, v in happens.items():
            ratio = int(v)/int(depth[k])
            name = f'{k[0]}→{k[-1]}'
            nameList.append(name)
            ratioList.append(ratio)

        if isBSM:
            condition = 'Base switching mutation'
        else:
            condition = 'Base transversion mutation'
        
        time.sleep(1)
        
        # Draw chart.
        print(f'Drawing Chart <{condition}>...')
        plt.figure()
        plt.bar(x=nameList, height=ratioList, width=0.5)
        plt.xticks(rotation=0)
        plt.ylabel('Ratio', fontsize=10)
        plt.xlabel(condition, fontsize=10)
        plt.title(f'{fileName}', fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(outputPath, f'{condition}_{fileName}.png'))
        time.sleep(1)

    # Combin chart.
    # Chart of Base switching mutation & Base transversion mutation.
    def summaryBSMandBTM(self, BSMhappens, BSMdepth, BTMhappens, BTMdepth, fileName, outputPath):
        import matplotlib.pyplot as plt
        import os, time

        tmpName = []
        tmpRatio = []
        nameList = ['A→G', 'G→A', 'C→T', 'T→C']
        ratioList = []

        # Prepare data for chart.
        print('Processing BSM data...')
        for k, v in BSMhappens.items():
            ratio = int(v)/int(BSMdepth[k])
            name = f'{k[0]}→{k[-1]}'
            tmpName.append(name)
            tmpRatio.append(ratio)

        print('Processing BTM data...')
        for k, v in BTMhappens.items():
            ratio = int(v)/int(BTMdepth[k])
            name = f'{k[0]}→{k[-1]}'
            tmpName.append(name)
            tmpRatio.append(ratio)

            condition = 'Base switching mutation & Base transversion mutation'
        
        # Set BSM to place 1,2,3,4.
        AGindex = tmpName.index('A→G')
        GAindex = tmpName.index('G→A')
        CTindex = tmpName.index('C→T')
        TCindex = tmpName.index('T→C')

        for elm in tmpName:
            if elm not in nameList:
                nameList.append(elm)
        
        ratioList.append(tmpRatio[AGindex])
        ratioList.append(tmpRatio[GAindex])
        ratioList.append(tmpRatio[CTindex])
        ratioList.append(tmpRatio[TCindex])

        for elm in tmpRatio:
            if elm not in ratioList:
                ratioList.append(elm)

        time.sleep(1)
        
        # Draw chart.
        print(f'Drawing Chart <{condition}>...')
        plt.figure()
        plt.bar(x=nameList, height=ratioList, width=0.5)
        plt.xticks(rotation=0)
        plt.ylabel('Ratio', fontsize=10)
        plt.xlabel(condition, fontsize=10)
        plt.title(f'{fileName}', fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(outputPath, f'BSMandBTM_{fileName}.png'))
        time.sleep(1)
