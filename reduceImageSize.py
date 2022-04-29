from skimage.transform import resize
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte
import pandas as pd
import math
import os

parisOutPath = "resized_paris/"
chenOutPath = "resized_chen/"
shanghaiOutPath = 'resized_shanghai/'

try:
    os.makedirs(parisOutPath)
    os.makedirs(chenOutPath)
    os.makedirs(shanghaiOutPath)
except:
    print("folders created already")

chenList = pd.read_pickle('chenimageNameLs.pkl')
parisList = pd.read_pickle('parisimageNameLs.pkl')
shanghaiList = pd.read_pickle('shanghaiimageNameLs.pkl')

targetLongestEdge = 340


# for i in chenList:
#     image = imread(i)
#     print(type(image[0][0][0]))
#     print(image.shape)
#     height = image.shape[0]
#     width = image.shape[1]
#     if (height > width):
#         width = math.ceil(width/height * targetLongestEdge)
#         height = targetLongestEdge
#     else:
#         height = math.ceil(height/width * targetLongestEdge)
#         width = targetLongestEdge        

#     image_resized = img_as_ubyte(resize(image, (height, width),anti_aliasing=True))
#     print(image_resized.shape)

    
#     import re
#     search = re.search("(?<=/)(.*)$",i)
#     filename = search.group()
#     filename = chenOutPath+filename
#     print(filename)
#     imsave(filename,image_resized)
    
for i in parisList:
    try:
        image = imread(i)
    except:
        continue
    print(type(image[0][0][0]))
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]
    if (height > width):
        width = math.ceil(width/height * targetLongestEdge)
        height = targetLongestEdge
    else:
        height = math.ceil(height/width * targetLongestEdge)
        width = targetLongestEdge        

    image_resized = img_as_ubyte(resize(image, (height, width),anti_aliasing=True))
    print(image_resized.shape)

    
    import re
    search = re.search("(?<=/)(.*)$",i)
    filename = search.group()
    filename = parisOutPath+filename
    print(filename)
    imsave(filename,image_resized)
    
# for i in shanghaiList:
#     image = imread(i)
#     print(type(image[0][0][0]))
#     print(image.shape)
#     height = image.shape[0]
#     width = image.shape[1]
#     if height >= targetLongestEdge or width >= targetLongestEdge:
#         if (height > width):
#             width = math.ceil(width/height * targetLongestEdge)
#             height = targetLongestEdge
#         else:
#             height = math.ceil(height/width * targetLongestEdge)
#             width = targetLongestEdge        

#         image_resized = img_as_ubyte(resize(image, (height, width),anti_aliasing=True))
#         print(image_resized.shape)
#     else:
#         image_resized = image
    
#     import re
#     search = re.search("(?<=/)(.*)$",i)
#     filename = search.group()
#     filename = shanghaiOutPath+filename
#     print(filename)
#     imsave(filename,image_resized)
    