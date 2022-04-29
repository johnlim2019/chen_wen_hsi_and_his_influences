import os 
from skimage.io import imread, imsave
path='paris/'
newpath = 'paris_short_name/'
imageLs = os.listdir(path)
imageLsOutput = []
for count,imgStr in enumerate(imageLs):
    imgLs = list(imgStr)
    #print(imgLs)
    index = imgLs.index('.')
    #print(index)
    name =imgLs[0:index][:15]
    nameStr = newpath+''.join(name)+("_"+str(count))+".jpg"
    print(nameStr)
    imageLsOutput.append(nameStr)

try:
    os.makedirs(newpath)
except:
    print("folder exists")

for index,file in enumerate(imageLsOutput):
    print(file)
    image = imread(path+imageLs[index])
    imsave(file,image)




