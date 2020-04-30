#sourcecode by Sourabh Choudhary https://stackoverflow.com/questions/24163421/twitter-user-profile-can-be-extracted-by-this
#user metadata twitter https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object.html

#Laden der benötigten Module

import tweepy
from tweepy import OAuthHandler

import csv

#Herstellen der Verbindung zur Twitter API über Keys und Access Tokens

consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

auth = OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
auth.set_access_token(access_token, access_token_secret)

#Vorbereitung csv-File

#Erstelle bzw. öffne Datei mit dem Namen userdata.csv, existierende Daten sollen nicht überschrieben werden, Daten sollen in UTF-8 kodiert werden


csvFile = open ("userdata_farbe.csv", "a", encoding="utf-8")


#Geschrieben werden soll in csvFile, Trennzeichen ist ;, \n markiert das Ende einer Datenreihe

csvWriter = csv.writer(csvFile, delimiter=";", lineterminator="\n")

#Gesucht werden sollen in tweepy.API nach Usern mit den Screennames Person 1 und Person 2

test = api.lookup_users(screen_names=[""])

# Ausgabe einzelner Userdaten (ID, Screenname, Name) von oben festgelegten Usern in Windows Eingabeaufforderung bzw. Mac/Linux Terminal sowie Schreiben einer Zeile mit den angegebenen Userdaten von Person 1 in userdata.csv (ID, Screenname, Name, Anzahl Follower, Anzahl Friends, Anzahl geposteter Statusmeldungen, Anzahl Listen, Ortung, Datum/Zeitpunkt der Accounterstellung, Sprache des Interface, User-URL, Biografie), dann weiterschreiben in neuer Zeile zu Userdaten von Person 2

for user in test:
	print(user.id)
	print(user.screen_name)
	print(user.name) 
	print(user.profile_link_color)
	csvWriter.writerow([user.id,user.screen_name,user.name,user.followers_count,user.friends_count,user.statuses_count,user.favourites_count,user.listed_count,user.location,user.geo_enabled,user.created_at,user.lang,user.url,user.description, user.profile_link_color, "\n"])