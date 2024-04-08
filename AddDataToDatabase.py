import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facemonitoringrealtime-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Students') #reference path of database

with open("AddDatabase.txt","r") as f:
    data = json.load(f)

for key,value in data.items():
    ref.child(key).set(value)