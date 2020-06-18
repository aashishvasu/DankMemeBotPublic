#Aashish Vasudevan
#Main file

from src.RedditHandler import RedditHandler
from src.TweetHandler import TweetHandler
from datetime import datetime, date, time, timedelta
from urllib.parse import urlparse
from random import randint
from pathlib import Path

import math
import os
import time
import sys
import requests

#Time Variables to decide next run
timeIntervalInHours = 6
nextRunHr = datetime.now()

def main():
    #Initialize MemeHandler with credentials
    meme = RedditHandler('reddit.json')

    #Initialize TweetHandler with login credentials
    tweetHandler = TweetHandler('twitter.json')

    #Define filename of text file in which all IDs are stored
    postFileName = "postID.txt"

    #File exception handling
    try:
        postFile = open(postFileName, 'r')
    except IOError:
        print("postID.txt not found, creating...")
        postFile = open(postFileName, 'w+')
        postFile.close()
        postFile = open(postFileName, 'r')

    #Get top post from the subreddit of your choice
    submission = meme.GetTopPosts('dankmemes', 10)
    post = ''

    #Get lines and close the file
    lines = postFile.readlines()
    postFile.close()

    #Check each line in the post file against each submission.
    #If there are any duplicates, keep iterating till we get one which is unique
    for i in submission:
        breakFor = False

        lineLength = len(lines)

        for l in lines:
            #Remove newline character fron code            
            l = l.strip('\n')

            #Iterate through each submission in list, if something similar is found, go to the next post
            if l != i.id:
                breakFor = True
            else:
                breakFor = False
                break
        if lineLength == 0:
            breakFor = True

        if breakFor == True:
            post = i
            break

    #Do string operations on the post and make it tweet-ready
    #Title
    tweet = ''
    tweet = post.title

    #Check if title is longer than 140 characters
    if len(tweet) >= 115:
        #write post ID to file and close it
        WriteAndSkip(post, postFileName)
        return


    #Url shortlink
    url = post.shortlink
    #Media url
    media = post.url

    #Get extension from url
    urlPath = urlparse(media).path
    ext = os.path.splitext(urlPath)[1]

    #Check if extensions are amongst those supported
    if ext != '.gif' and ext != '.png' and ext != '.jpg' and ext != '.jpeg':
        WriteAndSkip(post, postFileName)
        return

    #Initialize requests to download image from media url
    request = requests.get(media, stream=True)

    #If image is available, use it, else make a normal tweet
    filename = "temp" + ext
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

    # Check image size
    imgSize = math.ceil(Path(filename).stat().st_size/1024)
    if imgSize > 3075:
        print("Filesize too large, skipping")
        WriteAndSkip(post, postFileName)

    #Post tweet!
    if tweetHandler.PostTweetWithImageFromURL(tweet + "\n\n" + url, filename):
        #TODO: Add facebook posting

        #write post ID to file and close it
        postFile = open(postFileName, 'a')
        postFile.write('\n' + post.id)
        postFile.close()
    else:
        #Try again
        print("Posting failed!")
        return

    #Delete image file generated
    os.remove(filename)
#Write to file and execute main again in event of conflict to ignore file
def WriteAndSkip(post, postFileName):
    #write post ID to file and close it
    postFile = open(postFileName, 'a')
    postFile.write('\n' + post.id)
    postFile.close()
    main()

#Check current system time
def CheckSystemTime(nextRunTime):
    now = datetime.now()
    print(now.time())

    #Run main loop
    main()
    
#Run this based on time intervals
if __name__ == "__main__":
    #Run the main code and exit the file
    CheckSystemTime(nextRunHr)

    exit()