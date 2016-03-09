import sys
import json
import re
from operator import itemgetter


def extract_sentiment_values(sentiment_file_name):
    with open(sentiment_file_name) as sentiment_file:
        sentiment_data = {}
        for line in sentiment_file:
            term, sentiment = line.strip().split('\t')
            sentiment_data[term] = int(sentiment)

    return sentiment_data


def extract_tweets(tweet_file_name):
    with open(tweet_file_name) as tweet_file:
        tweet_list = [tweet.strip() for tweet in tweet_file.readlines()]

    tweets = []
    for tweet in tweet_list:
        tweet_json = json.loads(str(tweet))
        tweets.append(tweet_json)

    return tweets


def get_states(states_file_name):
    with open(states_file_name) as states_file:
        states = json.loads(states_file.read())
    return states


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


def compute_sentiment_for_tweets(tweets, sentiment_values):
    cumulative_sentiment = 0

    for tweet in tweets:
        _, sentiment_val = compute_sentiment(tweet, sentiment_values)
        cumulative_sentiment += sentiment_val

    avg_sentiment = cumulative_sentiment / len(tweets) if len(tweets) > 0 else 0
    return avg_sentiment


def get_us_state_from_place(tweet):
    location = None
    if tweet.get('place'):
        if tweet['place']['country_code'] == 'US':
            if tweet['place'].get('full_name'):
                location = tweet['place']['full_name']
    return location


def order_tweets_by_state(tweets):
    tweets_by_state = {}
    states = get_states('us_states.json')
    for tweet in tweets:
        location = get_us_state_from_place(tweet)
        
        if tweet.get('user'):
            if tweet['user'].get('location'):
                location = tweet['user']['location']
        elif tweet.get('retweeted_status'):
            location = get_us_state_from_place(tweet['retweeted_status'])

        if location:
            state = location.split(',')[-1].upper().strip()
            if state in states:
                if tweets_by_state.get(state):
                    tweets_by_state[state].append(tweet['text'])
                else:
                    tweets_by_state[state] = [tweet['text']]
    return tweets_by_state


def sort_results(state_sentiment_values):
    results = sorted(list(state_sentiment_values.items()), key=itemgetter(1, 0), reverse=True)
    return results


def main():
    sent_file_name = sys.argv[1]
    sentiment_data = extract_sentiment_values(sent_file_name)

    tweet_file_name = sys.argv[2]
    tweets = extract_tweets(tweet_file_name)

    tweets_by_state = order_tweets_by_state(tweets)

    sentiment_by_state = {}

    for state in tweets_by_state.keys():
        sentiment_by_state[state] = compute_sentiment_for_tweets(tweets_by_state[state], sentiment_data)

    results = sort_results(sentiment_by_state)

    for i in results:
        print(i[0] + '\t' + str(i[1]))


if __name__ == '__main__':
    main()
