import argparse
import oauth2 as oauth
import urllib.request as urllib
import json
import requests
import sys
import csv


access_token_key = "478809538-WkTRGB1E3ZUFh4YZhyO3yTpdsaNLy8kzYE0i3CjH"
access_token_secret = "5BKKRE1DjotYsBE9Jev13V8O7eLDYB2qewA3dSkcesdwC"

consumer_key = "6M3BsmWLbgJnGRZCIyPBBWs53"
consumer_secret = "hfrgEn95CUeYKjGbUyaqKs7p6QgSDaMVVA4dL6ZrGHGAaGE2mS"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

def fetch_samples():
    url = "https://stream.twitter.com/1.1/statuses/sample.json?language=en"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    with open('streaming_output_full.txt', 'w') as output_file:
        for line in response:
            tweet = json.loads(line.decode('utf-8').strip())
            output_file.write(json.dumps(tweet) + '\n')


def fetch_by_terms(term):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    parameters = [("q", term), ("count", 100)]
    response = twitterreq(url, "GET", parameters)
    print (response.readline())


def fetch_by_user_names(user_name_file):
    sn_file = open(user_name_file)
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    with open(user_name_file) as username_file:
        user_names = [username.strip() for username in username_file.readlines()]

    writer = csv.DictWriter(sys.stdout, fieldnames=['user_name', 'tweet'])
    writer.writeheader()

    for user_name in user_names:
        parameters = [("screen_name", user_name), ("count", 100)]
        response = twitterreq(url, "GET", parameters)
        for line in response:
            tweet_list = json.loads(line.decode('utf-8').strip())
            for tweet in tweet_list:
                row = {}
                if isinstance(tweet, str):
                    continue
                row['user_name'] = user_name
                row['tweet'] = tweet['text'].strip()
                writer.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', required=True, help='Enter the command')
    parser.add_argument('-term', help='Enter the search term')
    parser.add_argument('-file', help='Enter the user name file')
    opts = parser.parse_args()
    if opts.c == "fetch_samples":
        fetch_samples()
    elif opts.c == "fetch_by_terms":
        term = opts.term
        print (term)
        fetch_by_terms(term)
    elif opts.c == "fetch_by_user_names":
        user_name_file = opts.file
        fetch_by_user_names(user_name_file)
    else:
        raise Exception("Unrecognized command")
