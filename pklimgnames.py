#get list of all images for feature extraction
import os
path='images/'
imageLs = os.listdir(path)
imageLsOutput = []
for imgStr in imageLs:
    imgLs = list(imgStr)
    #print(imgLs)
    index = imgLs.index('.')
    #print(index)
    name =imgLs[0:index]
    nameStr = path+''.join(name)+".jpg"
    print(nameStr)
    imageLsOutput.append(nameStr)
import pickle
with open('chenimageNameLs.pkl', 'wb') as f:
    pickle.dump(imageLsOutput,f)

with open('chenimageNameLs.pkl', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    imgNameLs = pickle.load(f)
print(len(imgNameLs))
f.close()

path='paris/'
imageLs = os.listdir(path)
imageLsOutput = []
for imgStr in imageLs:
    imgLs = list(imgStr)
    #print(imgLs)
    index = imgLs.index('.')
    #print(index)
    name =imgLs[0:index]
    nameStr = path+''.join(name)+".jpg"
    print(nameStr)
    imageLsOutput.append(nameStr)


import re
newimgels =[]
# rename the paris images 
for source in imageLs:
    print(source)
    name = re.search("^(.)*(?=\.)",source)
    name = re.sub("\W","_",name.group())
    name = re.sub("_{2}","_",name)
    name = re.sub("_{2}","_",name)
    destination = path + name + ".jpg"
    newimgels.append(destination)
    print(name)
    try:
        os.rename(path+source,destination)
    except FileExistsError:
        print("desintation file exists")
    except FileNotFoundError:
        print("source file not found")

import pickle
with open('parisimageNameLs.pkl', 'wb') as f:
    pickle.dump(newimgels,f)

with open('parisimageNameLs.pkl', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    imgNameLs = pickle.load(f)
print(len(imgNameLs))
f.close()

import os
path='shanghai/'
imageLs = os.listdir(path)
imageLsOutput = []
for imgStr in imageLs:
    imgLs = list(imgStr)
    #print(imgLs)
    index = imgLs.index('.')
    #print(index)
    name =imgLs[0:index]
    nameStr = path+''.join(name)+".jpg"
    print(nameStr)
    imageLsOutput.append(nameStr)


import re
newimgels =[]
# rename the shanghai images 
for source in imageLs:
    print(source)
    name = re.search("^(.)*(?=\.)",source)
    name = re.sub("\W","_",name.group())
    name = re.sub("_{2}","_",name)
    name = re.sub("_{2}","_",name)
    destination = path + name + ".jpg"
    newimgels.append(destination)
    print(name)
    try:
        os.rename(path+source,destination)
    except FileExistsError:
        print("desintation file exists")
    except FileNotFoundError:
        print("source file not found")

import pickle
with open('shanghaiimageNameLs.pkl', 'wb') as f:
    pickle.dump(newimgels,f)

with open('shanghaiimageNameLs.pkl', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    imgNameLs = pickle.load(f)
print(len(imgNameLs))
f.close()
