from matplotlib.pyplot import figure

class drawChart():

    def __init__(self) -> None:
        pass

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
        plt.xlabel(condition, fontsize=10)
        plt.title(f'{title}_{fileName}', fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(outputPath, f'{title[:-4]}_{fileName}.png'))
        time.sleep(1)

        # Finish.
        print('Done')

    def drawBSMandBTM(self, happens, depth, isBSM, fileName, outputPath):
        import matplotlib.pyplot as plt
        import os, time

        nameList = []
        ratioList = []

        # Prepare data for chart.
        print('Processing data...')
        for k, v in happens.items():
            ratio = int(v)/int(depth[k])
            nameList.append(k)
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
