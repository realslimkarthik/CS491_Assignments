import re


def extract_sentiment_values(sentiment_file_name):
    with open(sentiment_file_name) as sentiment_file:
        sentiment_data = {}
        for line in sentiment_file:
            term, sentiment = line.strip().split('\t')
            sentiment_data[term] = int(sentiment)

    return sentiment_data


def _clean_word(word):
    cleaned_word = re.sub('(\b[^a-z]|[^a-z]\b)', '', word.lower())
    return cleaned_word.strip()


def _get_highest_n(sentiment_values):
    highest_n = 0
    for term in sentiment_values.keys():
        highest_n = len(term.split()) if len(term.split()) > highest_n else highest_n
    return highest_n


def _generate_n_gram(phrase, n):
    n_gram_phrase = []
    n1 = 0
    current_phrase = ''
    start_of_phrase = 0
    current_word_index = 0
    while start_of_phrase < len(phrase):
        try:
            word = phrase[current_word_index]
        except IndexError:
            break
        if n1 < n:
            current_phrase += word + ' '
            n1 += 1
            current_word_index += 1
        else:
            n_gram_phrase.append(current_phrase.strip())
            current_phrase = ''
            n1 = 0
            start_of_phrase += 1
            current_word_index = start_of_phrase

    return n_gram_phrase


def _compute_sentiment_by_phrase(phrases, sentiment_values):
    sentiment_value = 0

    for phrase in phrases:
        if sentiment_values.get(phrase):
            sentiment_value += sentiment_values[phrase]

    return sentiment_value


def compute_sentiment(text, sentiment_values):
    n = _get_highest_n(sentiment_values)
    current_n = 1
    sentiment_value = 0
    cleaned_text = [_clean_word(word) for word in text.split()]
    while current_n <= n:
        n_gram = _generate_n_gram(cleaned_text, current_n)
        sentiment_value += _compute_sentiment_by_phrase(n_gram, sentiment_values)
        current_n += 1

    return text, sentiment_value


