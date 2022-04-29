from fileinput import filename
from tkinter import image_names
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import pandas as pd 

def getURL():
    list=[]

    for pageNum in range(1,38):
        url = "https://chenwenhsi.com/gallery/page/{0}".format(pageNum)
        session = HTMLSession()
        page = session.get(url)

        #print(page.text)
        #with open("response.txt", "w") as f:
        #    f.write(page.text)
        soup = BeautifulSoup(page.content,"html.parser")
        list_tags = soup.find(class_="products columns-3")
        for i in list_tags:
            j = i.find('a')
            if (j == -1):
                continue
            print(j['href'])
            list.append(j['href'])
    print(len(list))
    return list

def download(list):
    imageInfoDf = pd.DataFrame(columns=['Title','SKU','Medium','Subject','Publication','url','File'])
    filelocation="images/"


    for index in range(0,len(list)):
        url = list[index]
        session = HTMLSession()
        page = session.get(url)
        soup = BeautifulSoup(page.content,"html.parser")
        # with open("imageresponse.txt", "w") as f:
        #    f.write(page.text)
        imgWrapper = soup.find(class_="woocommerce-product-gallery__wrapper")
        #print(imgWrapper)
        img = imgWrapper.find("img")
        print(img)
        print(img['data-src'])
        if img != -1:
            download = session.get(img['data-src'])
            filename = re.search("(?<=/)([\w\-\.\_]*)$",img['data-src']).group()
            title = re.search("(?<=/)([\w\-\_]*)(?=\.j)",img['data-src']).group()
            print(title)
            filename = filelocation + filename
            print(filename)
            open(filename, 'wb').write(download.content)
            # get the info 
            sku = soup.find("span",{"class":"sku"})
            sku = sku.contents[0]
            print(sku)
            additionalWrapper = soup.find(id="tab-additional_information")
            mediumWrapper = additionalWrapper.find("tr",{"class":"woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_medium"})
            medium = mediumWrapper.find("a").contents[0]
            print(medium)
            subjectWrapper = additionalWrapper.find("tr",{"class":"woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_subject"})
            subject = subjectWrapper.find("a").contents[0]
            print(subject)

            pubWrapper = additionalWrapper.find("tr",{"class":"woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_publication"})
            if pubWrapper != None:
                pub = pubWrapper.find(class_ ="woocommerce-product-attributes-item__value")
                pub = pub.contents[0]
            else:
                pub ="Not in a publication"
            print(pub)

            imageInfoDf.loc[index,"Title"] = title
            imageInfoDf.loc[index,"SKU"] = sku
            imageInfoDf.loc[index,"Medium"] = medium
            imageInfoDf.loc[index,"Subject"] = subject
            imageInfoDf.loc[index,"Publication"] = pub
            imageInfoDf.loc[index,"url"] = img['data-src']
            imageInfoDf.loc[index,"File"] = filename

        print(imageInfoDf)
    imageInfoDf = imageInfoDf.drop_duplicates(subset='File', keep='first')
    print(imageInfoDf.shape)
    return imageInfoDf

# ls = getURL()
# df = download(ls)
# df.to_csv("ImageData.csv")

df = pd.read_csv("ImageData.csv")
def download(df):
    urls = df['url']
    session = HTMLSession()
    image_names = df['File']
    print()
    for index,url in enumerate(urls):
        img = session.get(url)
        filename = image_names[index]
        print(filename)
        open(filename, 'wb').write(img.content)

download(df)


# url = "https://ntmofa-collections.ntmofa.gov.tw/en/Search.aspx?KEYWORD=KB5MKBKDMV52"
# session = HTMLSession()
# page = session.get(url)
# print(page.text)