import sys
import re
import json
from operator import attrgetter

def extract_tweets(tweet_file_name):
    with open(tweet_file_name) as tweet_file:
        tweet_list = [tweet.strip() for tweet in tweet_file.readlines()]

    tweets = []
    for tweet in tweet_list:
        tweet_json = json.loads(str(tweet))
        tweets.append(tweet_json['text'])

    return tweets


def extract_sentiment_values(sentiment_file_name):
    with open(sentiment_file_name) as sentiment_file:
        sentiment_data = {}
        for line in sentiment_file:
            term, sentiment = line.strip().split('\t')
            sentiment_data[term] = int(sentiment)

    return sentiment_data


def clean_word(word):
    non_character_regex = re.compile(r'[^a-zA-Z]')
    cleaned_word = non_character_regex.sub('', word.lower())
    return cleaned_word


def compute_sentiment(phrase, sentiment_values):
    sentiment_value = 0
    words_in_phrase = phrase.split()
    for word in words_in_phrase:
        cleaned_word = clean_word(word)
        if sentiment_values.get(cleaned_word):
            sentiment_value += sentiment_values[cleaned_word]

    return phrase, sentiment_value


def get_top_ten(tweet_sentiment_values, negative=False):
    top_ten = []
    top_ten_sentiment_values = []
    min_value = None

    if negative:
        old_tweet_sentiment_values = tweet_sentiment_values
        tweet_sentiment_values = [{'tweet': i['tweet'], 'sentiment_value': -1 * i['sentiment_value']} for i in old_tweet_sentiment_values]

    for tweet_sentiment_value in tweet_sentiment_values:
        if min_value is None:
            top_ten.append(tweet_sentiment_value)
            min_value = tweet_sentiment_value['sentiment_value']
        elif tweet_sentiment_value['sentiment_value'] > min_value:
            if len(top_ten) < 10:
                top_ten.append(tweet_sentiment_value)
            else:
                top_ten_sentiment_values = [i['sentiment_value'] for i in top_ten]
                min_index = top_ten_sentiment_values.index(min_value)
                top_ten[min_index] = tweet_sentiment_value
                top_ten_sentiment_values = [i['sentiment_value'] for i in top_ten]
                min_value = min(top_ten_sentiment_values)

    top_ten = sorted(top_ten, key=lambda i: (i['sentiment_value'], i['tweet']))

    if negative:
        top_ten = [{'tweet': i['tweet'], 'sentiment_value': -1 * i['sentiment_value']} for i in top_ten]
    else:
        top_ten.reverse()

    return top_ten


def main():
    sent_file_name = sys.argv[1]
    sentiment_data = extract_sentiment_values(sent_file_name)
    
    tweet_file_name = sys.argv[2]
    tweets = extract_tweets(tweet_file_name)

    tweets_sentiment_value = []
    for tweet in tweets:
        phrase, sentiment_value = compute_sentiment(tweet, sentiment_data)
        tweets_sentiment_value.append({'tweet': phrase, 'sentiment_value': sentiment_value})

    top_ten = get_top_ten(tweets_sentiment_value)
    bottom_ten = get_top_ten(tweets_sentiment_value, negative=True)
    
    for tweet in top_ten:
        print(tweet['tweet'] + '\t' + str(tweet['sentiment_value']))

    for tweet in bottom_ten:
        print(tweet['tweet'] + '\t' +  str(tweet['sentiment_value']))


if __name__ == '__main__':
    main()
