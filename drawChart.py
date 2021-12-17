from matplotlib.pyplot import figure


class drawChart():

    def __init__(self) -> None:
        pass

    def drawing(self, dict, title, outputPath, condition, fileName):
        from matplotlib.pyplot import MultipleLocator
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
        plt.bar(x=nameList, height=ratioList, width=0.5, color = 'pink')
        plt.xticks(rotation=90)
        plt.ylabel('Ratio', fontsize=10)
        plt.xlabel(condition, fontsize=10)
        plt.title(f'{title}_{fileName}', fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(outputPath, f'{title[:-4]}_{fileName}.png'))
        time.sleep(1)

        # Finish.
        print('Done')
