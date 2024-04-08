import os
import pickle
import threading
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
import time
import serial

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facemonitoringrealtime-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':'facemonitoringrealtime.appspot.com'
})

bucket = storage.bucket()
ser = serial.Serial('COM5', 9600, timeout=1)

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/PUPIL.png')

#Importing the mode images into the list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModeList)) #test number of images

def control_servo():
    try:
        if not ser.is_open:
            ser.open()  # Open the serial port if it's not already open

        ser.write(b'1')
        print("Servo turned 90 degrees")

        time.sleep(2)

        ser.write(b'1')
        print("Servo returned to the original position")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if ser.is_open:
            ser.close()


def put_text_threaded(img, text, position):
    cvzone.putTextRect(img, text, position)

def draw_student_info(imgBackground, studentInfo, id):
    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)  # Total Attendance text
    cv2.putText(imgBackground, str(studentInfo['section']), (1006, 550),
                cv2.FONT_HERSHEY_COMPLEX, 0.3, (100, 100, 100), 1)  # Section text
    cv2.putText(imgBackground, str(id), (1006, 493),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)  # ID text
    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)  # Standing
    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)  # year text
    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)  # Starting year text
    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
    offset = (414 - w) // 2
    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

def speak(text, rate=200):
    engine = pyttsx3.init()
    # Set the voice properties for a female voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Index 1 is usually a female voice
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

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

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                time.sleep(1)
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIDs[matchIndex]
                if counter == 0:
                    threading.Thread(target=put_text_threaded, args=(imgBackground, "Loading", (275, 400))).start()
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
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
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 100:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    threading.Thread(target=speak("Recipient Matched")).start()
                    threading.Thread(target=draw_student_info, args=(imgBackground, studentInfo, id)).start()
                    imgStudent = cv2.resize(imgStudent, (216, 216))  # Resize the student's image to fit the specified region
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                    threading.Thread(target=control_servo).start()
                    #cv2.waitKey(1)
                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break
cap.release()
cv2.destroyAllWindows()
