import sys
import csv
import re
from operator import itemgetter


def extract_actors_tweets(csv_file_name):
    with open(csv_file_name) as csv_file:
        file_reader = csv.DictReader(csv_file)
        actors_tweets = {}
        for row in file_reader:
            if actors_tweets.get(row['user_name']):
                actors_tweets[row['user_name']].append(row['tweet'])
            else:
                actors_tweets[row['user_name']] = [row['tweet']]

    return actors_tweets


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


def compute_sentiment_for_tweets(tweets, sentiment_values):
    cumulative_sentiment = 0

    for tweet in tweets:
        _, sentiment_val = compute_sentiment(tweet, sentiment_values)
        cumulative_sentiment += sentiment_val

    avg_sentiment = cumulative_sentiment / len(tweets)
    return avg_sentiment


def sort_results(actors_sentiment_scores):
    results = sorted(list(actors_sentiment_scores.items()), key=itemgetter(1, 0), reverse=True)
    return results


def main():
    sent_file_name = sys.argv[1]
    sentiment_data = extract_sentiment_values(sent_file_name)

    csv_file_name = sys.argv[2]
    actors_tweets = extract_actors_tweets(csv_file_name)

    actors_sentiment_scores = {}

    for actor in actors_tweets.keys():
        actors_sentiment_scores[actor] = compute_sentiment_for_tweets(actors_tweets[actor], sentiment_data)

    results = sort_results(actors_sentiment_scores)

    for i in results:
        print(i[0] + '\t' + str(i[1]))


if __name__ == '__main__':
    main()
