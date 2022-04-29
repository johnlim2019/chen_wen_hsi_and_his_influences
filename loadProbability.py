import math
import shutil
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import os
import pickle
import shutil
import re

from soupsieve import select

probablityDictLs=[]
file_check=0
path ='svc/'
for f in os.listdir(path):
    file = pd.read_pickle(path+f+'/probablity.pkl')
    file_check += len(os.listdir(path+f)) -1
    probablityDictLs.append(file)
# 0 is shanghai 
# 1 is paris 
print(file_check)

probabilityDict ={}
for i in probablityDictLs:
    probabilityDict.update(i[0])
with open('probabilityAll.pkl', 'wb') as f:
    pickle.dump(probabilityDict,f)
f.close()   

categoryDict={}
for i in probablityDictLs:
    categoryDict.update(i[1])
print(sum(categoryDict.values()))


#plotBar(probabilityDict,categoryDict,'all')

def buildDf(probabilityDict,categoryDict):
    imageData = pd.read_csv('ImageData.csv')
    category=[]
    shanghai_p = []
    paris_p =[]
    selectDf = imageData.loc[imageData['Title'].isin(probabilityDict.keys())]  
    for i in selectDf['Title']:
        category.append(categoryDict[i])
        shanghai_p.append(probabilityDict[i][0])
        paris_p.append(probabilityDict[i][1])
    selectDf['Category'] = category
    selectDf['shanghai_p'] = shanghai_p
    selectDf['paris_p'] = paris_p
    print(selectDf.shape)
    print(selectDf.columns)
    selectDf.drop(columns=['Unnamed: 0.1','Unnamed: 0'])
    selectDf.to_csv("ImageDataProbCat.csv")
    with open("imageDataProbCat.pkl","wb") as f:
        pickle.dump(select,f)
    f.close()


def findExtremes():
    imageData = pd.read_csv("ImageDataProbCat.csv")
    probabilityDf = imageData['shanghai_p']
    #print(probabilityDf.shape)
    npProbablityDf = probabilityDf.to_numpy()
    limit = np.percentile(npProbablityDf,90)
    print(limit)
    selectDf = imageData.loc[imageData['Category'] == 0]
    selectDf = selectDf.loc[selectDf['shanghai_p']>=limit]
    print(selectDf.shape)
    print()
    print('moving files')
    selectDf.to_csv('shanghaiExtremes.csv')
    try: 
        os.makedirs('shanghai_extremes/')   
    except:
        print("shanghai_extremes folder exists")
        dir = "shanghai_extremes/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        print("delete all previous images")
    for index,i in enumerate(selectDf['File']):
        j = re.search("(?<=/)(.*)$",i).group()
        j = str(round(selectDf.iloc[index,list(selectDf.columns).index('shanghai_p')],3))+"_"+j
        j='shanghai_extremes/'+j
        print(j)
        shutil.copyfile(i,j)
        
    probabilityDf = imageData['paris_p']
    #print(probabilityDf.shape)
    npProbablityDf = probabilityDf.to_numpy()
    limit = np.percentile(npProbablityDf,90)
    print(limit)
    selectDf = imageData.loc[imageData['Category'] == 1]
    selectDf = selectDf.loc[selectDf['paris_p']>=limit]
    selectDf.to_csv('parisExtremes.csv')
    print(selectDf.shape)
    print()
    print('moving files')
    try: 
        os.makedirs('paris_extremes/')   
    except:
        print("paris_extremes folder exists")
        dir = "paris_extremes/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        print("delete all previous images")
    for index,i in enumerate(selectDf['File']):
        j = re.search("(?<=/)(.*)$",i).group()
        j = str(round(selectDf.iloc[index,list(selectDf.columns).index('paris_p')],3))+"_"+j
        j='paris_extremes/'+j
        print(j)
        shutil.copyfile(i,j)
    
def findSvc():
    imageData = pd.read_csv("ImageDataProbCat.csv")
    selectDf = imageData.loc[imageData['Category'] == 0]
    selectDf = selectDf.loc[abs(selectDf['shanghai_p']-selectDf['paris_p']) <= 0.1]
    selectDf.to_csv('shanghaiClose.csv')
    print(selectDf.shape)
    print()
    print('moving files')
    try: 
        os.makedirs('shanghai_close/')   
    except:
        print("shanghai_close folder exists")
        dir = "shanghai_close/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        print("delete all previous images")
    for index,i in enumerate(selectDf['File']):
        j = re.search("(?<=/)(.*)$",i).group()
        j = str(round(selectDf.iloc[index,list(selectDf.columns).index('shanghai_p')],3))+"_"+selectDf.iloc[index,list(selectDf.columns).index('Subject')]+"_"+j
        j='shanghai_close/'+j
        print(j)
        shutil.copyfile(i,j)   
    selectDf = imageData.loc[imageData['Category'] == 1]
    selectDf = selectDf.loc[abs(selectDf['shanghai_p']-selectDf['paris_p']) <= 0.1]
    print(selectDf.shape)
    selectDf.to_csv('parisClose.csv')
    print()
    print('moving files')
    try: 
        os.makedirs('paris_close/')   
    except:
        print("paris_close folder exists")
        dir = "paris_close/"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        print("delete all previous images")        
    for index,i in enumerate(selectDf['File']):
        j = re.search("(?<=/)(.*)$",i).group()
        j = str(round(selectDf.iloc[index,list(selectDf.columns).index('paris_p')],3))+"_"+selectDf.iloc[index,list(selectDf.columns).index('Subject')]+"_"+j
        j='paris_close/'+j
        print(j)
        shutil.copyfile(i,j)   

buildDf(probabilityDict,categoryDict)
findExtremes()
findSvc()
