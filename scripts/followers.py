"""
Quelle: https://nocodewebscraping.com/extract-twitter-tweets-followers-excel/ bzw. Originaldatei ("followers_0.py") von https://drive.google.com/file/d/0Bw1LIIbSl0xuVkRuT1M2eXh5bjg/view

http://stackoverflow.com/questions/31000178/how-to-get-large-list-of-followers-tweepy
ask user for account name to harvest follower names from.
print follower names to screen
pause  users to screen
"""

#Laden der benötigten Module 

import tweepy
import time
import csv
import sys

#Herstellen der Verbindung zur Twitter API über Keys und Access Tokens

consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#zu analysierender Account

accountvar = ""

#Ausgabe von Datum und Uhrzeit -> ggf. hilfreich für Fehlläufe

print(time.strftime("%d.%m.%Y %H:%M:%S"))

#Ausgabe Info 

print("searching for followers of "+accountvar)

#Suche nach Followern in api.followers, von Person 1 und das Maximum innerhalb des rate limits (= max. 3000 Personen auf einmal)

users = tweepy.Cursor(api.followers, screen_name=accountvar, count=200).items()
count = 0
errorCount=0

#Rahmenbedingungen csv (Titel der Datei, ..., erste Reihe/Header)

outputfilecsv = accountvar+"followers.csv"
fc = csv.writer(open(outputfilecsv, 'w', encoding='utf-8'))
fc.writerow(["id", "screen_name","name","followers_count","friends_count","statuses_count","favourites_count","location","lang"])


while True:
	#finde jeweils den nächsten Follower aus der Liste
    try:
        user = next(users)
        count += 1
	#außer wenn Fehlermeldung tweepy.TweepError, dann warten bis die nächsten 3000 User geharvestet werden können 
    except tweepy.TweepError:
        print("sleeping....")
        time.sleep(60*16)
        user = next(users)
	#Ende des Loops:
    except StopIteration:
        break
    try:
        print("@" + user.screen_name + " has " + str(user.followers_count) +" followers, has made " + str(user.statuses_count)+" tweets and location=" + user.location + " count=" + str(count))
        fc.writerow([str(user.id), user.screen_name, user.name, str(user.followers_count),str(user.friends_count), str(user.statuses_count),str(user.favorites_count), user.location, str(user.lang)])
    except UnicodeEncodeError:
        errorCount += 1
        print("UnicodeEncodeError,errorCount ="+str(errorCount)) 


#apparently don't need to close csv.writer.
print("completed, errorCount ="+str(errorCount)+" total users="+str(count))
    #print "@" + user.screen_name
    #todo: write users to file, search users for interests, locations etc.