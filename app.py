import razorpay
import json,ast
import random
from firebase import Firebase
from flask import Flask, render_template, request
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAASNIN9qU:APA91bHwPAZyam3Uc4RZd2abDCeqj8Y8d8z-YR40EbnzaX98242piyWtuNn_WzGG1Rj4YTCid-1hJmtDT2Xle8gku65N32mMHdf5oKFPr6It5_npF7hbV7BzcUZSvEmmkhf-SOVTKQoN")



def rand_pass(len):
    pass_data = "qwertyuiopasdfgjklzxcvbnm1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    password = "".join(random.sample(pass_data, len))
    return password

true = True
false = False
null = None
app = Flask(__name__)

month_number = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November","12":"December"}

day_number = { "1":"Monday","2":"Tuesday","3":"Wednesday","4":"Thursday","5":"Friday","6":"Saturday","7":"Sunday" }

config = {
    "apiKey": "AIzaSyD-dljA9xatC5tY_xntrR1fMZZcv0H3qvM",
    "authDomain": "hackilo-edutech-contact-form.firebaseapp.com",
    "databaseURL": "https://hackilo-edutech-contact-form-default-rtdb.firebaseio.com",
    "projectId": "hackilo-edutech-contact-form",
   "storageBucket": "hackilo-edutech-contact-form.appspot.com",
    "messagingSenderId": "590022236783",
    "appId": "1:590022236783:web:75b6cbd0ebd67e23cccb9a",
    "measurementId": "G-LSNMWPXBNK"
  };

firebase = Firebase(config)
db = firebase.database()
razorpay_client = razorpay.Client(auth=("rzp_test_Y8FcD5KSf0vP0L", "hY7esVB4dayaRfLio8YnAes2"))

# https://www.dhitifoundation.android/aryomtech/S46iev8qgxXpkhl8al3USm0dlB92/-Mfw0sLrMOv63eJLF2CO
@app.route('/')
def app_create():

    return render_template('index.html')

@app.route('/aryomtech/<string:variable_1>/<string:variable_2>')
def aryomtech (variable_1,variable_2):
    global gl_push_key,gl_uid
    gl_push_key = variable_2
    gl_uid = variable_1
    return render_template('index.html')


@app.route('/charge', methods=['POST'])
def app_charge():
    amount = request.form.get("amount")*100
    print(amount)
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, amount)

    return "SUCCESS"

@app.route('/charges', methods=['POST'])
def app_charges():
    # push_key = "-Mfw0sLrMOv63eJLF2CO"
    # uid = "YOhEwrX0btQi6FiKGAdQiGBuA812"
    # uid = "S46iev8qgxXpkhl8al3USm0dlB92"
    push_key = gl_push_key
    uid = gl_uid
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, 50000)
    JSON_String_Payment = json.dumps(razorpay_client.payment.fetch(payment_id))
    JSON_Payment = json.loads(JSON_String_Payment)
    if JSON_Payment["status"]=="captured" and JSON_Payment["captured"]==True:
        in_push_key = "-M"+rand_pass(17)
        data={
            "amount_paid":"500",
            "key":in_push_key,
            "name":"MBSA CORP",
            "paid_on":"Saturday, 14 August 2021, 00:00 pm",
            "uid":uid,
        }
        db.child("fluid_Cards").child(push_key).child("transactions").child(in_push_key).set(data)
        db.child("fluid_Cards").child(push_key).child("raised_by_share").child(uid).child(in_push_key).set(data)
        cur_xp = db.child("users").child(uid).child("progress").child("xp").get().val()
        db.child("users").child(uid).child("progress").child("xp").set(cur_xp+15)
        device_token = db.child("users").child(uid).child("token").get().val()
        message_title = "Referral Successfull"
        message_body = "We got a confirmed donation from "+"BHAI BHAI"+" through your referral link.We are adding some points to your profile."
        result = push_service.notify_single_device(registration_id=device_token, message_title=message_title, message_body=message_body)
        return "SUCCESS"
    else:
        return "FAILURE"


