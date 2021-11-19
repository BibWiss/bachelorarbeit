import tweepy
import time
import csv
import sys

accountvar = ""

#todo: upgrade this to read usernames from a file.

print(time.strftime("%d.%m.%Y %H:%M:%S"))

print("searching for friends of ")

consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
#refer http://docs.tweepy.org/en/v3.2.0/api.html#API
#tells tweepy.API to automatically wait for rate limits to replenish


users = tweepy.Cursor(api.friends, screen_name=accountvar, count=200).items()
count = 0
errorCount=0


outputfilecsv = "friends.csv"
fc = csv.writer(open(outputfilecsv, 'w', encoding='utf-8'))
fc.writerow(["accountvar.screen_name", "id", "screen_name","name","followers_count","friends_count","statuses_count","favourites_count","location","lang"])

while True:
    try:
        user = next(users)
        count += 1
        #use count-break during dev to avoid twitter restrictions
        #if (count>10):
        #    break
    except tweepy.TweepError:
        #catches TweepError when rate limiting occurs, sleeps, then restarts.
        #nominally 15 minnutes, make a bit longer to avoid attention.
        print("sleeping....")
        time.sleep(60*16)
        user = next(users)
    except StopIteration:
        break
    try:
         print("@" + user.screen_name +  " has " + str(user.followers_count) +\
              " followers, has made "+str(user.statuses_count)+" tweets and location=" +\
              user.location+" count="+str(count))
   
         fc.writerow([accountvar, str(user.id), user.screen_name, user.name, str(user.followers_count),str(user.friends_count), str(user.statuses_count),str(user.favourites_count), user.location, str(user.lang)])
    except UnicodeEncodeError:
        errorCount += 1
        print("UnicodeEncodeError,errorCount ="+str(errorCount)) 


#apparently don't need to close csv.writer.
print("completed, errorCount ="+str(errorCount)+" total users="+str(count))

