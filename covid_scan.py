#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:28:08 2020

@author: maxwell
"""

import praw
import datetime
import os
import requests
import config
import csv

def bot_login():
    """
    This function logs in the bot account that I am using to access Reddit.

    Returns
    -------
    bot : TYPE
        DESCRIPTION.

    """
    bot = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "My COVID-19 mention scanning bot")
    return bot


def run_bot(bot):
    """
    

    Parameters
    ----------
    bot : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    
    """
    subreddits = ("worldnews", "news", "funny", "gaming", "pics", "science", 
                  "videos", "AskReddit", "aww", "askscience", "Tinder")
    output = {
        "worldnews" : 0,
        "news" : 0, 
        "funny" : 0, 
        "gaming" : 0, 
        "pics" : 0, 
        "science" : 0,                  
        "videos" : 0, 
        "AskReddit" : 0, 
        "aww" : 0, 
        "askscience" : 0, 
        "Tinder" : 0
        }
    print("*"*80)
    print(" "*10 + "Running Coronavirus mention scan")
    print("*"*80+"\n")
    print("-"*80)
    for subreddit in subreddits:       
        print("Scanning r/" + subreddit + "\n")
        count = 0
        current = bot.subreddit(subreddit)
        cutoff_time = datetime.date.today() - datetime.timedelta(1)
        cutoff_time = float(cutoff_time.strftime("%s"))
        for submission in current.new():
            if submission.created_utc > cutoff_time:
                current_title = submission.title.lower()
                if "coronavirus" in current_title:
                    count += 1
                    print(submission.title + "\n")
        output[subreddit] = count
        print("Total mentions of Coronavirus in r/" + subreddit + ":", count)
        print("-"*80)
    write_output(output)
        
        
def write_output(output):
    """
    

    Parameters
    ----------
    output : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    with open("results.csv", 'a') as f:
        
            


if __name__ == '__main__':
    bot = bot_login()
    run_bot(bot)
