#Aashish Vasudevan
#Class to load the top post from given subreddit, and return appropriate values

import praw
import json

class RedditHandler():

    #The main instance of reddit
    reddit = None

    #Initialize this class
    def __init__(self, fileName):
        print("Authenticating Twitter")
        jsonObj = ''
        with open(fileName) as f:
            jsonObj = json.load(f)

        self.StartAuth(jsonObj['client_id'], jsonObj['client_secret'], jsonObj['user_agent'])
    
    #Returns top post from the given subreddit
    def GetTopPosts(self, subredditName, num):
        #Get reference to the subreddit to perform sub related tasks
        subreddit = self.reddit.subreddit(subredditName)

        #Return top posts
        submission = subreddit.top('day', limit=num)
        return submission

    #Initializes praw and assigns it to a reusable reddit module
    def StartAuth(self, cID, cSecret, uAgent):
        self.reddit = praw.Reddit(client_id = cID, client_secret = cSecret, user_agent = uAgent)