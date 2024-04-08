import cv2
import face_recognition
import pickle
import os

#Importing the parent's images
folderParentPath = 'ParentImages'
ParentPathList = os.listdir(folderParentPath)
imgParentList = []
parentIds = []
for path in ParentPathList:
    imgParentList.append(cv2.imread(os.path.join(folderParentPath,path)))
    parentIds.append(os.path.splitext(path)[0])

def findParentEncodings(parentimageList):
    parentencodeList = []
    for img2 in parentimageList:
        img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        parentencode = face_recognition.face_encodings(img2)[0]
        parentencodeList.append(parentencode)

    return parentencodeList

print("Parent Encoding Started....")
parentencodeListKnown = findParentEncodings(imgParentList)
parentencodeListKnownWithIDs = [parentencodeListKnown,parentIds]
print("Parent Encoding Complete")

file = open("ParentEncoderFile.p",'wb')
pickle.dump(parentencodeListKnownWithIDs,file)
file.close()
print("file saved")