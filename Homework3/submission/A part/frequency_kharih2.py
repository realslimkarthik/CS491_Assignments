import sys
import json


def remove_stopwords(tweet, stopwords):
    tweet_words = tweet.split()
    tweet_without_stopwords = []
    for word in tweet_words:
        cleaned_word = word.strip().strip('.').strip(',').strip('?').strip(':').strip(';')
        if cleaned_word.lower() not in stopwords and cleaned_word != '':
            tweet_without_stopwords.append(cleaned_word)
    return tweet_without_stopwords


def compute_term_frequency(tweet_list):
    term_counts = {}
    term_frequencies = {}
    for tweet in tweet_list:
        for term in tweet:
            if term_counts.get(term):
                term_counts[term] += 1
            else:
                term_counts[term] = 1

    total_count_of_terms = sum(count for term, count in term_counts.items())

    for term, count in term_counts.items():
        term_frequency = count / total_count_of_terms
        term_frequencies[term] = term_frequency

    return term_frequencies


def main():
    stopword_file_name = sys.argv[1]
    with open(stopword_file_name) as stopword_file:
        stopwords = {stopword.strip(): 1 for stopword in stopword_file.readlines()}

    tweet_file_name = sys.argv[2]
    with open(tweet_file_name) as tweet_file:
        tweet_list = [tweet.strip() for tweet in tweet_file.readlines()]

    tweets = []
    for tweet in tweet_list:
        tweet_json = json.loads(str(tweet))
        tweets.append(tweet_json['text'])

    tweets_without_stopwords = [remove_stopwords(tweet, stopwords) for tweet in tweets]
    term_frequencies = compute_term_frequency(tweets_without_stopwords)

    row = '{0}\t{1:.10f}'

    for term, frequency in term_frequencies.items():
        print(row.format(term, frequency))
    

if __name__ == '__main__':
    main()