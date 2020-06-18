#Aashish Vasudevan
#A class to tweet something using links, images, and text. Wraps around the status based uses of tweepy

import tweepy
import os
import json

class TweetHandler(object):
    
    #Reference to tweepy.API which is used to do most of the work
    twtr = None

    #Initialize this class
    def __init__(self, fileName):
        print("Authenticating Twitter")
        jsonObj = ''
        with open(fileName) as f:
            jsonObj = json.load(f)

        self.StartAuth(jsonObj['client_key'], jsonObj['client_secret'], jsonObj['token_key'], jsonObj['token_secret'])

    #Initialize the tweepy wrapper using the authentication values from the site
    def StartAuth(self, cKey, cSecret, tKey, tSecret):
        auth = tweepy.OAuthHandler(cKey, cSecret)
        auth.set_access_token(tKey, tSecret)

        #Set the API reference and authenticate it
        self.twtr = tweepy.API(auth)

    #Post tweet using the contents of the string
    def PostTweet(self, string):
        self.twtr.update_status(string)

    #Post tweet using text it has recieved, and an image from either a local path or a URL
    def PostTweetWithImageFromURL(self, string, media):
        
        #Check if file exists
        if(os.path.isfile(media)):
            self.twtr.update_with_media(media, string)
            print("posted " + string + "\n**********************\n\n")
            return True
        else:
            print("No image could be loaded!")
            return False