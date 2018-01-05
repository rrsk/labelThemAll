import numpy as np
import ntpath
import cv2 as cv
import os

#global variables
folder = "NFPA dataset"
idxs = []

#class to store objects 
class Box:
    def __init__(self,image,_list=[]):
        self.i = image
        self.l = _list

#storing the images to their corresponding indexes / file name and
#returning the list of all Box objects
def load_images_from_folder(folder):
    images = {}
    
    for filename in os.listdir(folder):
        idx = os.path.splitext(filename)[0]
        img = cv.imread(os.path.join(folder,filename))
        if img is not None:
            image = img
            b = Box(image=image)
            images[idx]=b
            idxs.append(idx)

    return images


#create lists of all the arrays described as text and storing them against
#the indxes 
def fill_lists(folder,images):
    for filename in os.listdir(folder):
        idx = os.path.splitext(filename)[0]
        list2 =[]
        # Split the extension from the path and normalise it to lowercase.
        ext = os.path.splitext(filename)[-1].lower()
        _path=os.path.join(folder, filename)

        # Now we can simply use == to check for equality, no need for wildcards.
        if ext == ".txt":
            text_file = open(_path, "r")
            _list = text_file.read().split('\n')
            for i in range(len(_list)-1):
                list2.append(_list[i].split(' '))
            
            try:
                images[idx].l = list2
            except:
                pass
    return



# RUNNING the defined functions for the given data  
images = load_images_from_folder(folder)
fill_lists(folder,images)



# Finally calculating and storing the results of the data
for i in range(len(idxs)):
    print(i,idxs[i])
    img = cv.imread(folder+"/"+idxs[i]+".jpg")
    if img is None:
        img = cv.imread(folder+"/"+idxs[i]+".JPG")
    elif img is None:
        continue
    H = np.size(img,0)
    W = np.size(img,1)
    D = np.size(img,2)

    try:
        os.stat("OutputLabels")
    except:
        os.mkdir("OutputLabels")

    file = open("OutputLabels/"+idxs[i]+".xml","w")
    s = '''<annotation>
    <folder>'''+ str(folder) +'''</folder>
    <filename>pos-33.jpg</filename>
    <path>''' + str(os.getcwd()) + '''/'''+str(folder)+'''/'''+idxs[i]+''''.jpg</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>'''+str(W)+'''</width>
        <height>'''+str(H)+'''</height>
        <depth>'''+str(D)+'''</depth>
    </size>'''


    for j in images[idxs[i]].l:
        x = float(j[1])
        y = float(j[2])
        w = float(j[3])
        h = float(j[4])
        img = cv.rectangle(img, (int((x-w/2)*W),int((y-h/2)*H)),(int((x+w/2)*W),int((y+h/2)*H)), (0,0,255), 5)
        s += '''
        <object>
            <name>nfpa</name>
            <pose>Unspecified</pose>
            <truncated>0</truncated>
            <difficult>0</difficult>
            <bndbox>
                <xmin>'''+str(int((x-w/2)*W))+'''</xmin>
                <ymin>'''+str(int((y-h/2)*H))+'''</ymin>
                <xmax>'''+str(int((x+w/2)*W))+'''</xmax>
                <ymax>'''+str(int((y+h/2)*H))+'''</ymax>
            </bndbox>
        </object>'''
        
    try:
        os.stat("OutputImages")
    except:
        os.mkdir("OutputImages")
    cv.imwrite(str("OutputImages/"+idxs[i])+".jpg",img)
    s+='''
    </annotation>'''
    file.write(s)
    file.close()

