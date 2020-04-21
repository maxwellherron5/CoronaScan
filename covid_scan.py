#!/Users/maxwell/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:28:08 2020

@author: maxwell
"""

import praw
import datetime
import config
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

subreddits = ("worldnews", "news", "funny", "gaming", "pics", "science",
                  "videos", "AskReddit", "aww", "askscience", "Tinder",
                  "BlackPeopleTwitter", "politics", "dankmemes", "memes",
                  "PoliticalHumor", "WhitePeopleTwitter", "ABoringDystopia")

def bot_login():
    """
    This function logs in the bot account that I am using to access Reddit.
    """
    bot = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "My COVID-19 mention scanning bot")
    return bot


def run_bot(bot):
    """
    This here is the meat and potatoes. I'll explain later . . .
    """
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
        "Tinder" : 0,
        "BlackPeopleTwitter" : 0,
        "politics" : 0,
        "dankmemes" : 0,
        "PoliticalHumor" : 0,
        "memes" : 0,
        "WhitePeopleTwitter" : 0,
        "ABoringDystopia" : 0
        }
    print("*"*80)
    print(" "*10 + "Running COVID-19 keyword mention scan")
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
                keyword_check = ("coronavirus" in current_title or
                                "covid" in current_title or
                                "pandemic" in current_title or
                                "quarantine" in current_title)
                if keyword_check:
                    count += 1
                    print(submission.title + "\n")
        output[subreddit] = count
        print("Total mentions of COVID-19 related keywords in r/" + subreddit + ":", count)
        print("-"*80)
    write_output(output)


def write_output(output):
    """
    Writes the output dictionary generated from run_bot() to the existing CSV
    """
    with open("/Users/maxwell/Documents/workspace/CoronaScan/results.csv", 'a') as f:
        writer = csv.writer(f)
        print("Now writing output to results.csv . . .")
        values = list(output.values())
        values.insert(0, datetime.date.today())
        writer.writerow(values)
        print("Finished writing output!")


def print_daily_report():
    """

    """



def generate_day_comparison():
    """
    Generates a bar graph based upon the findings of the current day.
    """
    df = pd.read_csv("results.csv", names=[i for i in subreddits])
    #fig = plt.figure()
    #counts = df.iloc[1]
    #print(counts)

    #print(counts)
    #ax.bar(subreddits, counts)
    #plt.show()



if __name__ == '__main__':
    bot = bot_login()
    run_bot(bot)
    #generate_day_comparison()
