#!/Users/maxwell/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:28:08 2020

This module runs locally everyday at 11:59 PM central time. It parses through
the given subreddits and looks for mentions of COVID-19 related keywords.
It then writes the number of mentions per subreddit to a master CSV, and
hopefully soon will make some neat plots with the data.

Author: Maxwell Herron
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
                  "PoliticalHumor", "WhitePeopleTwitter", "ABoringDystopia",
                  "Conservative", "nottheonion", "LateStageCapitalism")

# This is the day that data collection began. It will be used to calculate
# the offset necessary to determine which row of the CSV to plot.
start_day = datetime.date(2020, 4, 23)

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
    output = {key: None for key in subreddits}
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


def get_offset():
    """
    Calculates the integer offset between the start day of data collection,
    and the current day. This is then used to determine which line of the CSV
    to generate the plot from.
    """
    offset = datetime.date.today() - start_day
    return int(offset.days)


def generate_day_comparison():
    """
    =========
    Bar Graph
    =========
    Generates a bar graph based upon the findings of the current day. It then
    saves the graph as a .png in the plots directory.
    """
    df = pd.read_csv("/Users/maxwell/Documents/workspace/CoronaScan/results.csv",
                     names=[i for i in subreddits])

    row_values = df.to_numpy()
    counts = row_values[get_offset() + 1]
    vals = []
    for i in counts:
        vals.append(int(i))
    plt.rcParams['xtick.major.pad']='8'
    N = len(subreddits)
    fig, chart = plt.subplots()
    index = np.arange(N)
    width = 0.35
    plot = chart.bar(index, vals, width)
    for i, v in enumerate(vals):
        chart.text(i-.2, v/(vals[i]+100), vals[i], fontsize=11)

    chart.set_xticks(index)
    chart.set_xticklabels(subreddits, rotation=45, ha='right', minor=False, fontsize=8)
    chart.set_xlabel("Subreddit", fontsize=14)
    chart.set_ylabel("Number of Mentions", fontsize=14)
    chart.set_title("Keyword Mentions by Subreddit on " +
                    str(datetime.date.today()), fontsize=20, pad=20)

    plt.tight_layout()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig("/Users/maxwell/Documents/workspace/CoronaScan/plots/" +
                str(datetime.date.today()), bbox_inches='tight')



if __name__ == '__main__':
    bot = bot_login()
    run_bot(bot)
    generate_day_comparison()
