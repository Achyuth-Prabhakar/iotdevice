import wiotp.sdk.device
import time
import random
import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "XXXXX sender_mail XXXXX"
    msg['from'] = user
    password = "XXX password_after_setting_up_two-factor-auth XXXXXX"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


myConfig = { 
    "identity": {
        "orgId": "XXXXXXX",
        "typeId": "XXXXXXXXX",
        "deviceId":"XXXXXXX"
    },
    "auth": {
        "token": "XXXXXXXXXXXXXXXX"
    }
}

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

while True:
    temp=random.randint(0,50)
    hum=random.randint(0,50)
    duration=random.randint(1,5)
    if duration == 5 :
        email_alert ("ALERT", "You have been standing in the radiation for too long", "XXXXXXX res_mail XXXXX")
    uSvh=round(random.uniform(0,1),2)
    cpm=round(random.uniform(1,5),2)
    myData={'temperature':temp, 'humidity':hum,'duration':duration, 'uSvh':uSvh, 'cpm':cpm}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    client.commandCallback = myCommandCallback
    time.sleep(2)
client.disconnect()
