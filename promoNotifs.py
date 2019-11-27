{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from datetime import datetime, timedelta, date\n",
    "import time\n",
    "import slack\n",
    "import json\n",
    "\n",
    "#uses slack to tag users and notify them of their promo task\n",
    "#key = user, value = task\n",
    "def notify(key, value):\n",
    "    user = ids[key]\n",
    "    response = sc.chat_postMessage(\n",
    "        channel='#general',\n",
    "        text='Hey <@' + user + '>, please promo: ' + value + '!')\n",
    "    assert response[\"ok\"]\n",
    "    assert response[\"message\"][\"text\"] == 'Hey <@' + user + '>, please promo: ' + value + '!'\n",
    "\n",
    "#for users who have tasks on date, call notify\n",
    "def who_to_notif(df, date):\n",
    "    datedict = df.loc[:,date].to_dict()\n",
    "    for key, value in datedict.items():\n",
    "        if value != 0:\n",
    "            notify(key, value)\n",
    "\n",
    "#filenames and google sheet link to read\n",
    "apiFile = \"FILE.txt\"\n",
    "idFile = \"FILE.json\"\n",
    "oglink = 'INSERT LINK HERE'\n",
    "            \n",
    "#read api key & setup client\n",
    "with open(apiFile, \"r\") as file:\n",
    "    secret = file.read()\n",
    "sc = slack.WebClient(secret)\n",
    "\n",
    "#read user ids\n",
    "with open(idFile, \"r\") as file:\n",
    "    ids = json.load(file)\n",
    "\n",
    "#convert and parse spreadsheet\n",
    "split_og = oglink.split('/')\n",
    "new_link = ''\n",
    "for i in range (0,6):\n",
    "    new_link += split_og[i] + '/' \n",
    "df = pd.read_csv( new_link + 'export?gid=0&format=csv', parse_dates=True)\n",
    "df.drop(df.columns[[1]], axis=1, inplace=True)\n",
    "df1 = df.fillna(0)\n",
    "df1 = df1.set_index('Exec')\n",
    "df1.columns = pd.to_datetime(df1.columns, format='%m/%d/%Y') + timedelta(hours=21)\n",
    "\n",
    "#run this system for the entire promo schedule\n",
    "zero = datetime.timedelta(0)\n",
    "i = 0\n",
    "while i<len(df1.columns):\n",
    "    diff = df1.columns[i].to_pydatetime()-date.today()\n",
    "    if diff >= zero:\n",
    "        #wait until next promo day at 9pm to notify the user\n",
    "        time.sleep(diff.total_seconds())\n",
    "        who_to_notif(df1, df1.columns[i])\n",
    "    i += 1"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}