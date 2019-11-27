import pandas as pd
from datetime import datetime, timedelta, date
import time
import slack
import json

#uses slack to tag users and notify them of their promo task
#key = user, value = task
def notify(key, value):
    user = ids[key]
    response = sc.chat_postMessage(
        channel='#general',
        text='Hey <@' + user + '>, please promo: ' + value + '!')
    assert response["ok"]
    assert response["message"]["text"] == 'Hey <@' + user + '>, please promo: ' + value + '!'

#for users who have tasks on date, call notify
def who_to_notif(df, date):
    datedict = df.loc[:,date].to_dict()
    for key, value in datedict.items():
        if value != 0:
            notify(key, value)

#filenames and google sheet link to read
apiFile = "FILE.txt"
idFile = "FILE.json"
oglink = 'INSERT LINK HERE'
            
#read api key & setup client
with open(apiFile, "r") as file:
    secret = file.read()
sc = slack.WebClient(secret)

#read user ids
with open(idFile, "r") as file:
    ids = json.load(file)

#convert and parse spreadsheet
split_og = oglink.split('/')
new_link = ''
for i in range (0,6):
    new_link += split_og[i] + '/' 
df = pd.read_csv( new_link + 'export?gid=0&format=csv', parse_dates=True)
df.drop(df.columns[[1]], axis=1, inplace=True)
df1 = df.fillna(0)
df1 = df1.set_index('Exec')
df1.columns = pd.to_datetime(df1.columns, format='%m/%d/%Y') + timedelta(hours=21)

#run this system for the entire promo schedule
zero = datetime.timedelta(0)
i = 0
while i<len(df1.columns):
    diff = df1.columns[i].to_pydatetime()-date.today()
    if diff >= zero:
        #wait until next promo day at 9pm to notify the user
        time.sleep(diff.total_seconds())
        who_to_notif(df1, df1.columns[i])
    i += 1