# A reddit bot that posts book names, chapters, and wiki pages for characters
# and quotes of the book series "Wheel of time"
# This information is extracted from the wheel of time wiki page: http://wot.wikia.com/wiki/
# Created by Jon-Pierre Hanna (Chosengamer)

from bs4 import BeautifulSoup #Seems especially redundent
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4 #This seams redundent with line 6?

#Location of file where id's of already visited comments are maintained. Might need to double check file path
path = "/commented.txt"

#Text to be posted along side book titles, chapter etc.
header1 = "**Detected ta'veren, collecting profile:**\n"
header2 = "**Found memory of a ta'veren, providing description:**"
footer = "\n*--This info was extracted from the [A wheel of time wikia](wot.wikia.com/wiki/)| Bot created by u/chosengamer | [Source Code] (~to be inserted~)*"
#Insert github link above

def authenticate():
    
    print('Authenticating...\n')
    reddit = praw.Reddit('DragonRebot', user_agent = 'web:DragonRebot:v0.1 (by /u/chosengamer)')#Will need to double check the user_agent input
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit
    
def fetchdata(url):
    r =requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #currently is only looking for daily quotes, will need to use if else, or something similar for each different type of information
    tag = soup.find('em')#find and insert tag here
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            #This will need to be edited based on how the page is read
            if (tag.name == 'h2'):
                break
            if (tag.name == 'h3'):
                tag = tag.nextSibling
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling
    return data
    
def run_dragonrebot(reddit):
    
    print("Getting 250 comments...\n")
    
    #change subreddit later, should also figure out how to exclude subreddits
    for comment in reddit.subreddit('test').comments(limit=250):
        #need to figure out normal expression format for when the bot will run, and what info it will search for
        match = re.findall(, comment.body)
        if match:
            print("Quote found in comment with comment ID: " + comment.id)
            wotQuote=match[0]
            
            
            try:
                quote_data = fetchdata()