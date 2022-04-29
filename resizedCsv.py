import pandas as pd
dataframe = pd.read_csv('ImageData.csv')

for index,name in enumerate(dataframe['File']):
    name = name.replace('images','resized_chen')
    dataframe['File'].loc[index] = name
    print(dataframe['File'].loc[index])

dataframe.to_csv('ImageDataResized.csv')