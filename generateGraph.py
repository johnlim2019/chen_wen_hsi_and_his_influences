import shutil
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import os
import pickle
import shutil
import re

def plotScatter(probabilityDict,categoryDict,subject):
    shanghai =[]
    paris = []
    for i in categoryDict:
        if categoryDict[i] == 1:
            shanghai.append([probabilityDict[i][0],probabilityDict[i][1]])
        else:
            paris.append([probabilityDict[i][0],probabilityDict[i][1]])
    shanghai = np.array(shanghai)
    paris = np.array(paris)
    print(len(shanghai))
    print(len(paris))
    # x is for shanghai prob
    # y is for paris prob
    shanghai_x = shanghai[:,0]
    shanghai_y = shanghai[:,1]
    paris_x = paris[:,0]
    paris_y = paris[:,1]
    x_p = [paris_x,shanghai_x]
    y_p = [paris_y,shanghai_y]

    #print(x_p[:10])
    #print(y_p[:10])
    color = np.array(['b','y'])
    fig, ax = plt.subplots()
    legend = ['Paris','Shanghai']
    for index,title in enumerate(legend):
        x = x_p[index]
        y = y_p[index]
        ax.scatter(x,y,c=color[index],alpha=0.3,label=title)
    ax.legend()
    ax.grid(True)
    ax.set_title(subject)
    plt.xlabel('Shanghai_p')
    plt.ylabel('Paris_p')
    folder = "svc_plots/"
    try:
        os.makedirs(folder)
    except:
        pass
    fig.savefig(folder+subject+'.svg')
    fig.savefig(folder+subject+'.png')
    plt.show()
    return

#plotScatter(probabilityDict,categoryDict,'all')

def plotBar(probabilityDict,categoryDict,subject):
    shanghai =[]
    paris = []
    labels = list(probabilityDict.keys())
    for i in categoryDict:
        shanghai.append(probabilityDict[i][0])
        paris.append(probabilityDict[i][1])
    shanghai = np.array(shanghai)
    paris = np.array(paris)
    print(len(shanghai))
    print(len(paris))
    print(len(labels))
    fig, ax = plt.subplots()
    ax.bar(labels,shanghai)
    ax.bar(labels,paris,bottom=shanghai)
    folder = "svc_plots/"
    try:
        os.makedirs(folder)
    except:
        pass
    fig.savefig(folder+subject+'.svg')
    fig.savefig(folder+subject+'.png')
    plt.show()  
    return

imageData = pd.read_csv("ImageDataProbCat.csv")
shanghai_p = imageData.loc[imageData['Category'] == 0]['shanghai_p']
paris_p = imageData.loc[imageData['Category'] == 1]['paris_p']
equal = shanghai_p.loc[shanghai_p == 0.5]
print(equal.shape)
shanghai_p = shanghai_p.loc[shanghai_p != 0.5]
print(shanghai_p.shape)
print(paris_p.shape)

print('paris_p')
Q3 = np.quantile(paris_p, 0.75)
Q1 = np.quantile(paris_p, 0.25)
IQR = Q3 - Q1
print(paris_p.mean(),paris_p.std(),IQR)

print('shanghai')
Q3 = np.quantile(shanghai_p, 0.75)
Q1 = np.quantile(shanghai_p, 0.25)
IQR = Q3 - Q1
print(shanghai_p.mean(),shanghai_p.std(),IQR)

shanghai_p = imageData.loc[imageData['Category'] == 0]['Subject']
chenSubjects = ['Heron','Duck','Gibbon','Chicken','Sparrow','Lotus','Landscape','Koi Fish']
for i in chenSubjects:
    temp = shanghai_p.loc[shanghai_p == i]
    print(i)
    print(temp.shape)
    print()