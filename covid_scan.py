#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:28:08 2020

@author: maxwell
"""

import scrapy as sp
import praw
import time
import os
import requests
import config
import pandas

def bot_login():
    """
    This function logs in the bot account that I am using to access Reddit.

    Returns
    -------
    bot : TYPE
        DESCRIPTION.

    """
    print("Loggin in...")
    bot = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "My COVID-19 mention scanning bot")
    print("Logged in!")
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
    
    
    print("Running COVID-19 mention scan")
    
    for subreddit in subreddits:
        print("-"*80)
        print("Scanning r/" + subreddit)
        print("-"*80)
        current = bot.subreddit(subreddit)
        for submission in current.hot():
            current_title = submission.title.lower()
            if "coronavirus" in current_title:
                print(submission.title + "\n")
            
    


if __name__ == '__main__':
    bot = bot_login()
    run_bot(bot)
