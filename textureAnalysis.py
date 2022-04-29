import numpy as np
import pandas as pd
from scipy import ndimage as nd
import pickle

from skimage.io import imread
from skimage.util import img_as_ubyte
from skimage.filters import gabor_kernel
from skimage.feature import graycomatrix, graycoprops
from skimage.color import rgb2gray
import imageio


#frequency is the spaital separation of the pixels, groups of pixels to be considered
#theta is the orientation angle in radians 0 is the leftdirection
#sigma is the standard deviation x and y,

#print(len(kernels))

def compute_gabor(image,kernels,savePath,fileName):
    import re,os
    search = re.search('^(.*)(?=/)',fileName)
    print(savePath+search.group()+"/")
    try:
        os.makedirs(savePath+search.group()+"/")
    except:
        pass
    print("computing gabor")
    listgabor = []
    fileName = fileName[:-4]
    for k, kernel in enumerate(kernels):
        filtered = nd.convolve(image, kernel, mode='wrap')
        listgabor.append(filtered)
        title = savePath+fileName+"_"+str(k)+".jpg"
        print(title)
        imageio.imwrite(title,filtered)
    print("filtered imgs list length")
    print(len(listgabor))        
    return listgabor

def compute_glcm(listgabor,longestedgetargetsize):
    print("computing glcm")
    height = listgabor[0].shape[1]
    width = listgabor[0].shape[0]
    if height>width: 
        longest = height
    else:
        longest = width
    hops = longest/longestedgetargetsize
    listglcm =[]
    angles =[0] 
    print("angles for glcm")
    print(angles)
    print("distances for glcm")
    print(hops)
    print("shape of matrices")
    for i in listgabor:
        matrix = graycomatrix(i,[hops],angles)
        print(matrix.shape)
        listglcm.append(matrix)
    
    print("number of matrices")
    print(len(listglcm))
    return listglcm

def compute_properties(listglcm,kernels,angles):
    print("computing glcm property")
    # number of cols, is number of filters * number of features * angles in glcm
    output_np_array = np.zeros(len(kernels)*6*len(angles))
    for index,i in enumerate(listglcm):
        contrast = graycoprops(i,"contrast")
        #print(contrast.shape)
        contrast = np.reshape(contrast,[len(angles)])
        #print(contrast.shape)
        #contrast = graycoprops(contrast,"contrast")
        #print(contrast)
        dissimilarity = graycoprops(i,"dissimilarity")
        dissimilarity = np.reshape(dissimilarity,[len(angles)])
        #dissimilarity = graycoprops(dissimilarity,"dissimilarity")        
        #print(dissimilarity)
        homogeneity = graycoprops(i,"homogeneity")
        homogeneity = np.reshape(homogeneity,[len(angles)])   
        #homogeneity = graycoprops(homogeneity,"homogeneity")        
        asm = graycoprops(i,"ASM")
        asm = np.reshape(asm,[len(angles)])
        #print(asm)
        #asm = graycoprops(asm,"ASM")        
        correlation = graycoprops(i,"correlation")
        correlation = np.reshape(correlation,[len(angles)])
        #print(correlation)
        #correlation = graycoprops(correlation,"correlation")
        energy = np.round(np.sqrt(asm),0)
        #print(energy)
        curr_filter_arr = np.concatenate([contrast,dissimilarity,homogeneity,asm,correlation,energy])
        #curr_filter_arr = curr_filter_arr.reshape(curr_filter_arr,[len(angles)*6])
        output_np_array[index*6*len(angles):index*6*len(angles)+6*len(angles)] = curr_filter_arr
        return output_np_array


def compute_feats(image, kernels,longestedgetargetsize):
    print("output order for each image, glcm features * glcm angles * filter")
    print("this is flattened into long vector")
    print("computing gabor glcm")
    # finding pixel ratio
    height = image.shape[1]
    width = image.shape[0]
    if height>width: 
        longest = height
    else:
        longest = width

    hops = longest/longestedgetargetsize
    listgabor = []
    for k, kernel in enumerate(kernels):
        filtered = nd.convolve(image, kernel, mode='wrap')
        listgabor.append(filtered)
    print("filtered imgs list length")
    print(len(listgabor))
    listglcm =[]
    angles = []
    for i in range(4):
        angles.append(i/4*np.pi)
    print("angles for glcm")
    print(angles)
    print("distances for glcm")
    print(hops)
    print("shape of matrices")
    for i in listgabor:
        matrix = graycomatrix(i,[hops],angles)
        print(matrix.shape)
        listglcm.append(matrix)
    
    print("number of matrices")
    print(len(listglcm))
    print("glcm property")
    # number of cols, is number of filters * number of features * angles in glcm
    output_np_array = np.zeros(len(kernels)*6*len(angles))
    for index,i in enumerate(listglcm):
        contrast = graycoprops(i,"contrast")
        #print(contrast.shape)
        contrast = np.reshape(contrast,[len(angles)])
        #print(contrast.shape)
        #contrast = graycoprops(contrast,"contrast")
        #print(contrast)
        dissimilarity = graycoprops(i,"dissimilarity")
        dissimilarity = np.reshape(dissimilarity,[len(angles)])
        #dissimilarity = graycoprops(dissimilarity,"dissimilarity")        
        #print(dissimilarity)
        homogeneity = graycoprops(i,"homogeneity")
        homogeneity = np.reshape(homogeneity,[len(angles)])   
        #homogeneity = graycoprops(homogeneity,"homogeneity")        
        asm = graycoprops(i,"ASM")
        asm = np.reshape(asm,[len(angles)])
        #print(asm)
        #asm = graycoprops(asm,"ASM")        
        correlation = graycoprops(i,"correlation")
        correlation = np.reshape(correlation,[len(angles)])
        #print(correlation)
        #correlation = graycoprops(correlation,"correlation")
        energy = np.round(np.sqrt(asm),0)
        #print(energy)
        curr_filter_arr = np.concatenate([contrast,dissimilarity,homogeneity,asm,correlation,energy])
        #curr_filter_arr = curr_filter_arr.reshape(curr_filter_arr,[len(angles)*6])
        output_np_array[index*6*len(angles):index*6*len(angles)+6*len(angles)] = curr_filter_arr
    return output_np_array


def process_images(list,targetHistSize,numangles,frequency):
    dict ={}
    kernels = []
    error = []
    for theta in range(numangles):
        theta = theta / numangles * np.pi 
        print("kernel hyperparameters")
        print(theta,frequency)
        kernel = np.real(gabor_kernel(frequency, theta=theta))
        kernels.append(kernel)
    print(len(list))
    for i in list:
        print()
        print(i)
        print()
        try:
            img = img_as_ubyte(rgb2gray(imread(i)))
            print("image shape")
            print(img.shape)
        except: 
            print("ERROR")
            print(i)
            error.append(i)

        print("\ntarget hist size")
        print(targetHistSize)
        print()
        try:
            fd = compute_feats(img,kernels,targetHistSize)
            print(fd.shape)
            dict[i] = fd
        except:
            error.append(i)
    print(error)
    return dict
    

def main():
    numangles = 4
    frequency = 0.05
    kernels =[]
    for theta in range(numangles):
        theta = theta / numangles * np.pi 
        print("kernel hyperparameters")
        print(theta,frequency)
        kernel = np.real(gabor_kernel(frequency, theta=theta))
        kernels.append(kernel)
    
    # chenDf = pd.read_pickle('chenimageResizedNameLs.pkl')    
    # print(len(chenDf))    
    # chenDict = process_images(chenDf,512,numangles,frequency)
    # print(len(chenDict))
    # with open('chenResizedGlcmValues.pkl', 'wb') as f:
    #     pickle.dump(chenDict,f)
    # f.close()

    parisDf = pd.read_pickle("parisimageResizedNameLs.pkl")    
    print(len(parisDf))
    parisDict = process_images(parisDf,512,numangles,frequency)
    print(len(parisDict))
    with open("parisResizedGlcmValues.pkl","wb") as f:
        pickle.dump(parisDict,f)
    f.close()
    for i in parisDf:
        try:
            img = img_as_ubyte(rgb2gray(imread(i)))
        except:
            continue 
        compute_gabor(img,kernels,'gabor_filter/',i)

    #shanghaiDf = pd.read_pickle('shanghaiimageResizedNameLs.pkl')
    # print(len(shanghaiDf))
    
    # for i in shanghaiDf:
    #     try:
    #         img = img_as_ubyte(rgb2gray(imread(i)))
    #     except:
    #         continue 
    #     compute_gabor(img,kernels,'gabor_filter/',i)

    # shanghaiDict = process_images(shanghaiDf,512,numangles,frequency)
    # print(len(shanghaiDict))
    # with open("shanghaiResizedGlcmValues.pkl","wb") as f:
    #     pickle.dump(shanghaiDict,f)
    # f.close()
main()

# kernels = []
# kernelparam = []
# for theta in range(4):
#     theta = theta / 4. * np.pi # 0, 45, 90, 135
#     for frequency in (0.05, 0.25):
#         print("kernel hyperparameters")
#         print(theta,frequency)
#         kernelparam.append((theta,frequency))
#         kernel = np.real(gabor_kernel(frequency, theta=theta))
#         kernels.append(kernel)
# imgName = "images/chen-wen-hsi-assembling-chickens.jpg"
# img = img_as_ubyte(rgb2gray(imread(imgName)))
# #print(img.shape)
# print("num of kernels")
# print(len(kernels))
# #print(kernels[0].shape)
# feat = compute_feats(img,kernelparam,kernels,512)
# print(len(feat))
