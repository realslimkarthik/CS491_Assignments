import sys
import csv
import re
from operator import itemgetter
from phrase_sentiment import extract_sentiment_values, compute_sentiment


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
