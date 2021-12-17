from matplotlib.pyplot import colorbar


class drawChart():
    def __init__(self) -> None:
        pass

    def drawing(self, dict, title, outputPath):
        import matplotlib.pyplot as plt
        import os

        nameList = []
        ratioList = []

        # Prepare data for chart.
        print('Processing data...')
        for key in dict.keys():
            top = dict[key]['happens']
            bottom = dict[key]['depth']
            
            nameList.append(key)
            ratioList.append(top/bottom)
        
        # Draw chart.
        print('Charting...')
        plt.bar(x=nameList, height=ratioList, width=0.5, color = 'pink')
        plt.ylabel('Ratio')
        plt.title(title)
        plt.savefig(os.path.join(outputPath, f'{title[:-4]}.png'))

        # Finish.
        print('Done')
