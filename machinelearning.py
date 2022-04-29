# read the files
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.svm import SVC
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import os
import pickle

def prepare_array(inputDict):
    print(type(inputDict))
    height = len(inputDict)
    print(height)
    print(type(inputDict[list(inputDict.keys())[0]]))
    targetLen = inputDict[list(inputDict.keys())[0]].shape[0]
    print(targetLen)
    counter =0

    for i in inputDict:
        #print(len(inputDict[i]))
        #print(inputDict[i].shape)
        try:
            assert inputDict[i].shape[0] == targetLen
        except:
            print("Wrong length")
            print(i)
            return
        counter+=1
    print(counter)
    print("all images have correct length of features")
    output_array = np.zeros((height,targetLen))
    print(output_array.shape)    
    for index,i in enumerate(inputDict):
        output_array[index][:] = inputDict[i]
    #print(output_array[0][:])
    return output_array

def normalise(chen,paris,shanghai):
    input_dict = dict(chen)
    input_dict.update(paris)
    input_dict.update(shanghai)
    output_array = np.zeros([len(input_dict),input_dict[list(input_dict.keys())[0]].shape[0]])
    for index,key in enumerate(input_dict.keys()):
        output_array[index][:] = input_dict[key]
    output_array = normalize(output_array,axis=0)        
    print(output_array.shape)
    print([len(input_dict),input_dict[list(input_dict.keys())[0]].shape[0]])
    for index,key in enumerate(input_dict.keys()):
        input_dict[key] = output_array[index][:]
    print([len(input_dict),input_dict[list(input_dict.keys())[0]].shape[0]])
    chen_out = {key: input_dict[key] for key in input_dict.keys() if key in list(chen.keys())}
    paris_out = {key: input_dict[key] for key in input_dict.keys() if key in list(paris.keys())}
    shanghai_out = {key: input_dict[key] for key in input_dict.keys() if key in list(shanghai.keys())}
    return chen_out,paris_out,shanghai_out

def prepare_array_chen(input_dict,chen_data,subject,medium="Chinese Ink on Paper"):
    print()
    subject_list = list(chen_data['Subject'])
    print(type(subject_list))
    print(subject in subject_list)
    medium_list = list(chen_data['Medium'])
    print(medium in medium_list)
    if ((subject in subject_list)*(medium in medium_list) == 0):
        print("subject/medium not in data")
        return
    select_images_dict = {}
    print("select artworks with images")
    select_df = chen_data.loc[chen_data['File'].isin(list(input_dict.keys()))]
    print(select_df.shape)
    select_df = select_df.loc[select_df['Medium'] == medium]
    print("select medium")
    print(select_df.shape)
    select_df = select_df.loc[select_df['Subject'] == subject]
    print("select subject")
    #print(select_df.shape)
    image_names = select_df["Title"]
    count=0
    for name in image_names:
        #print(name)
        count+=1
        select_images_dict[name] = input_dict[images+name+".jpg"]
    #print(count)
    output_array = np.zeros([len(select_images_dict),select_images_dict[list(select_images_dict.keys())[0]].shape[0]])
    print("target height")
    print(len(select_images_dict))
    print("target width")
    print(select_images_dict[list(select_images_dict.keys())[0]].shape[0])
    for index,name in enumerate(select_images_dict):
        output_array[index][:] = select_images_dict[name]
    print(output_array.shape)
    return output_array, select_df

def build_model(paris,shanghai):
    print("target size")
    print(len(paris) + len(shanghai))
    X =  np.vstack((paris,shanghai))
    print(X.shape)
    #print("normalise")
    #X = normalize(X,axis=0)
    Y = np.zeros((X.shape[0]))
    for index,i in enumerate(paris):
        Y[index] = 1
    try:
        assert np.sum(Y) == len(paris)
    except:
        print("screwed up")
        return
    clf = SVC(probability=True,random_state=872323141)
    clf.fit(X,Y)
    return clf
def predict(model,source_array,data_df,location):
    #source_array = normalize(source_array,axis=0)
    #predict_y = model.predict(source_array)
    #print(model.classes_)
    probDict={}
    catDict={}
    predict_proba_y = model.predict_proba(source_array)

    predict_y_bool = predict_proba_y[:,0] < predict_proba_y[:,1]
    floatMap = map(int, predict_y_bool)
    predict_y = list(floatMap)

    import shutil
    count = 0
    for index,i in enumerate(data_df['Title']):
        source_path = 'images/'+i+".jpg"
        count +=1
        #print(source_path)
        dest_path = location+str(int(predict_y[index]))+"_"+i+'.jpg'
        #print(dest_path)
        shutil.copy(source_path,dest_path)
        probDict[i] = predict_proba_y[index]
        catDict[i] = predict_y[index]
        #print(count)
    with open(location+'probablity.pkl', 'wb') as f:
        pickle.dump((probDict,catDict),f)
    f.close()  
    print(len(predict_y))      
    print(predict_y)
    print(sum(predict_y))
    return predict_y

# change which values to use
images ='resized_chen/'
chenNameLs = pd.read_pickle('chenimageResizedNameLs.pkl')
parisDict = pd.read_pickle('parisResizedGlcmValues.pkl')
chenDict = pd.read_pickle('chenResizedGlcmValues.pkl')
shanghaiDict = pd.read_pickle('shanghaiResizedGlcmValues.pkl')
chen_csv_df = pd.read_csv('ImageDataResized.csv')
# images ='images/'
# chenNameLs = pd.read_pickle('chenimageNameLs.pkl')
# parisDict = pd.read_pickle('parisgmlcmvalues.pkl')
# chenDict = pd.read_pickle('chenglcmvalues.pkl')
# shanghaiDict = pd.read_pickle('shanghaiglcmvalues.pkl')
# chen_csv_df = pd.read_csv('ImageData.csv')
print(chen_csv_df.shape)
print(len(chenNameLs))

chenDict,parisDict,shanghaiDict = normalise(chenDict,parisDict,shanghaiDict)

parisArray = prepare_array(parisDict)
shanghaiArray = prepare_array(shanghaiDict)
chen_heron_array,heron_df = prepare_array_chen(chenDict,chen_csv_df,"Heron")
chen_duck_array, duck_df = prepare_array_chen(chenDict,chen_csv_df,"Duck")
chen_gibbon_array, gibbon_df = prepare_array_chen(chenDict,chen_csv_df,"Gibbon")
chen_chicken_array,chicken_df = prepare_array_chen(chenDict,chen_csv_df,"Chicken")
chen_sparrow_array,sparrow_df = prepare_array_chen(chenDict,chen_csv_df,"Sparrow")
chen_lotus_array,lotus_df = prepare_array_chen(chenDict,chen_csv_df,"Lotus")
chen_landscape_array,landscape_df = prepare_array_chen(chenDict,chen_csv_df,"Landscape")

chenSubjects = ['Heron','Duck','Gibbon','Chicken','Sparrow','Lotus','Landscape','Koi Fish']
chenSubjectDict = {}
for i in chenSubjects:
    array,df = prepare_array_chen(chenDict,chen_csv_df,i)
    chenSubjectDict[i] = (array,df)
print(chenSubjectDict.keys())

model = build_model(parisArray,shanghaiArray)
for i in chenSubjectDict.keys():
    foldername= "svc/"+i.lower().replace(" ","_")+"/"
    print(foldername)
    try:
        os.mkdir(foldername)
        print("folder "+ foldername +" is made")
    except:
        print("folder "+ foldername +" exists")
        dir = foldername
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        print("delete all previous images")
    predict(model,chenSubjectDict[i][0],chenSubjectDict[i][1],foldername)






def set_tsne(paris,shanghai,chenDict):
    builder_tsne = TSNE(n_components=2, learning_rate='auto',init='pca')
    nanyang = np.zeros([len(chenDict),chenDict[list(chenDict.keys())[0]].shape[0]])
    print(nanyang.shape)
    for index,name in enumerate(chenDict):
        nanyang[index][:] = chenDict[name]
    array =  np.vstack([paris,shanghai,nanyang])
    #array = normalize(array,axis=0)
    print(array.shape)

    array_reduce = builder_tsne.fit_transform(array)      
    array_reduce_paris = array_reduce[0:paris.shape[0],:]
    print("paris shape")
    print(array_reduce_paris.shape)
    array_reduce_shanghai = array_reduce[paris.shape[0]:paris.shape[0]+shanghai.shape[0],:]
    print("shanghai shape")
    print(array_reduce_shanghai.shape)
    chen_tsne_dict = {}
    for index,i in enumerate(chenDict.keys()):
        #print(i)
        chen_tsne_dict[i] = array_reduce[paris.shape[0]+shanghai.shape[0]+index,:]
    print("size of chen dict")
    print(len(chen_tsne_dict.keys()))
    return array_reduce_paris, array_reduce_shanghai, chen_tsne_dict

def plot_tsne(paris,shanghai,chen_tsne_dict,chen_data_df,subject='all'):
    paris_x = paris[:,0]
    paris_y = paris[:,1]
    shanghai_x = shanghai[:,0]
    shanghai_y = shanghai[:,1]
    select_df = chen_data_df.loc[chen_data_df['Medium'] == "Chinese Ink on Paper"]
    print("select medium")
    print(select_df.shape)
    if subject != 'all':
        select_df = select_df.loc[select_df['Subject'] == subject]
    print("select subject")
    #print(select_df.shape)
    image_names = select_df["Title"]
    select_images_dict ={}
    for name in image_names:
        #print(name)
        select_images_dict[name] = chen_tsne_dict[images+name+".jpg"]
    print(len(select_images_dict.keys()))
    nanyang = np.zeros((len(select_images_dict.keys()),2))
    for index,i in enumerate(select_images_dict.keys()):
        nanyang[index,:] = select_images_dict[i]
    print(nanyang.shape)
    nanyang_x = nanyang[:,0]
    nanyang_y = nanyang[:,1]        
    x = [paris_x,shanghai_x,nanyang_x]
    y = [paris_y,shanghai_y,nanyang_y]
    color = np.array(['b','y','r'])
    fig, ax = plt.subplots()
    legend = ['Paris','Shanghai','Nanyang']
    for index,title in enumerate(legend):
        xx = x[index]
        yy = y[index]
        ax.scatter(xx,yy,c=color[index],alpha=0.3,label=title)
    ax.legend()
    ax.grid(True)
    ax.set_title(subject)
    tsne = "tsne/"
    try:
        os.makedirs(tsne)
    except:
        pass
    fig.savefig(tsne+subject+'.svg')
    fig.savefig(tsne+subject+'.png')

    return 

paris,shanghai,nanyangDict = set_tsne(parisArray,shanghaiArray,chenDict)
print("return testing")
print(paris.shape)
print(shanghai.shape)
print(len(nanyangDict))
print(len(nanyangDict[list(nanyangDict.keys())[0]]))

chenSubjects = ['Heron','Duck','Gibbon','Chicken','Sparrow','Lotus','Landscape','Koi Fish']
for subject in chenSubjects:
    print(subject)
    plot_tsne(paris,shanghai,nanyangDict,chen_csv_df,subject)
plot_tsne(paris,shanghai,nanyangDict,chen_csv_df,'all')

