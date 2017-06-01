import os
import sys
from random import choice
import twitter

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
    access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    # print ' '.join(words[:140])
    long_string_of_words = " ".join(words)
    under_140_chars = long_string_of_words[:140]

    return under_140_chars



def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.



    status = api.PostUpdate(make_text(chains))
    print status

    tweet_again = raw_input('\nWould you like to tweet again? Enter to tweet again or q to quit: ')

    while tweet_again[0] != 'q':
        tweet(chains)
# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt


filenames = sys.argv[1:]
# could also use text below to request user input of a .txt file instead of argv
# filenames = raw_input("What file would you like to use for your Markov chain? ")

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# print make_text(chains)

# Your task is to write a new function tweet, that will take chains as input
tweet(chains)

