import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facemonitoringrealtime-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':'facemonitoringrealtime.appspot.com'
})


#Importing the student images
folderPath = 'Images'
modePathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in modePathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0]) #Remove the png in the images
#print(len(imgList)) #test number of images
#print(studentIds)

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName) #Send data image data over here

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print('encoding started')
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIDs = [encodeListKnown, studentIds]
print(encodeListKnown)
print('encoding complete')

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIDs,file)
file.close()
print('File Saved')