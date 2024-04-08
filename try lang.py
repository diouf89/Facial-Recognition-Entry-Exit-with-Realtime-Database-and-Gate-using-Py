import os
import threading
import pickle
import cvzone
import cv2
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import pyttsx3
import  pyautogui
import time

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facemonitoringrealtime-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':'facemonitoringrealtime.appspot.com'
})

bucket = storage.bucket()

folder_path = r"C:\Users\diouf\PycharmProjects\pythonProject6\Screenshots"
file_name = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.png"

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
cap2 = cv2.VideoCapture(2)
cap2.set(3, 640)
cap2.set(4, 480)

imgBackground = cv2.imread('Resources/bak2.jpg')

#Importing the mode images into the list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModeList)) #test number of images

def draw_student_info(imgBackground, studentInfo, id):
    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (800, 102),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)  # Total Attendance text
    cv2.putText(imgBackground, str(studentInfo['section']), (950, 532),
                cv2.FONT_HERSHEY_COMPLEX, 0.3, (100, 100, 100), 1)  # Section text
    cv2.putText(imgBackground, str(id), (950, 475),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)  # ID text
    cv2.putText(imgBackground, str(studentInfo['standing']), (815, 635),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)  # Standing
    cv2.putText(imgBackground, str(studentInfo['year']), (930, 635),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)  # year text
    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1015, 635),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)  # Starting year text

    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
    offset = (414 - w) // 2
    cv2.putText(imgBackground, str(studentInfo['name']), (760 + offset, 420),
                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

def take_screenshot_and_save(folder_path, file_name):
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to the specified folder and filename
    screenshot.save(f"{folder_path}/{file_name}")


def put_text_threaded(img, text, position):
    cvzone.putTextRect(img, text, position)

def speak(text, rate=200):
    engine = pyttsx3.init()
    # Set the voice properties for a female voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Index 1 is usually a female voice
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

print("Loading Parent File...")
parentfile = open('ParentEncoderFile.p', 'rb')
parentencodeListKnownWithIDs = pickle.load(parentfile)
parentfile.close()
parentencodeListKnown, parentIds = parentencodeListKnownWithIDs
print(parentIds)
print("Parent File Loaded...")

#Load the encoding file
print('Loading Encode File...')
file = open('EncodeFile.p','rb')
encodeListKnownWithIDs = pickle.load(file)
file.close()
encodeListKnown, studentIDs = encodeListKnownWithIDs
#print(studentIDs)
print("Encode File Loaded...")


modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    success2, img2 = cap2.read()

    imgP = cv2.resize(img2, (0, 0), None, 0.25, 0.25)
    imgP = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img2 = cv2.resize(img2, (640, 480))  # Resize for Camera to prevent error
    imgS = cv2.resize(img, (0,0),None,0.25,0.25) #Resize photo image
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Change Color

    faceCurFrame = face_recognition.face_locations(imgS) #Old image
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame) #New image compare
    parentCurFrame = face_recognition.face_locations(imgP)
    parentencodeCurFrame = face_recognition.face_encodings(imgP, parentCurFrame)

    img = cv2.resize(img, (600, 450))  # Adjust dimensions to match the region
    img2 = cv2.resize(img2, (600, 450))  # Resize for Camera to prevent error
    imgBackground[154:154 + img.shape[0], 44:44 + img.shape[1]] = img
    imgBackground[154:154 + img.shape[0], 1277:1277 + img.shape[1]] = img2
    imgBackground[27:27 + 633, 751:751 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for (parentencodeFace, parentfaceLoc), (encodeFace, faceloc) in zip(zip(parentencodeCurFrame, parentCurFrame),
                                                                            zip(encodeCurFrame, faceCurFrame)):
            parentmatches = face_recognition.compare_faces(parentencodeListKnown, parentencodeFace)
            parentfaceDis = face_recognition.face_distance(parentencodeListKnown, parentencodeFace)
            parentmatchIndex = np.argmin(parentfaceDis)
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                time.sleep(1)
                y1, x2, y2, x1 = faceloc
                x, y, w, h = x1+50, y1 + 200, x2 - x1, y2 - y1 # +50 is to shift the bbox to the right and +200 to shift downward
                bbox = (x, y, w, h)
                imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
                id = studentIDs[matchIndex]
                if counter == 0:
                    threading.Thread(target=put_text_threaded, args=(imgBackground, "Loading", (300,400))).start()
                    threading.Thread(target=put_text_threaded, args=(imgBackground, "Loading", (1500, 400))).start()
                    cv2.waitKey(1)
                    cv2.imshow("Face Monitoring System",imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1 and parentIds[parentmatchIndex] == studentIDs[matchIndex]:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 9000:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    threading.Thread(target=speak("Already Marked")).start()
                    modeType = 3
                    counter = 0
                    cv2.waitKey(1)
                    imgBackground[27:27 + 633, 751:751 + 414] = imgModeList[modeType]

            if counter == 1 and parentIds[parentmatchIndex] != studentIDs[matchIndex]:
                threading.Thread(target=take_screenshot_and_save(folder_path, file_name)).start()
                threading.Thread(target=speak("Recipient not matching")).start()
                modeType = 0
                counter = 0
                #print(parentIds[parentmatchIndex])
                cv2.waitKey(1)
                continue

            if modeType != 3:

                if 10 < counter < 100:
                    modeType = 2

                imgBackground[27:27 + 633, 751:751 + 414] = imgModeList[modeType]

                if counter <= 10:
                    threading.Thread(target=speak("Recipient Matched")).start()
                    threading.Thread(target=draw_student_info, args=(imgBackground, studentInfo, id)).start()
                    imgStudent = cv2.resize(imgStudent, (216, 216))  # Resize the student's image to fit the specified region
                    imgBackground[158:158 + 216, 851:851 + 216] = imgStudent
                    #cv2.waitKey(1)
                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[27:27 + 633, 751:751 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Monitoring System", imgBackground)
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break
cap.release()
cv2.destroyAllWindows()
