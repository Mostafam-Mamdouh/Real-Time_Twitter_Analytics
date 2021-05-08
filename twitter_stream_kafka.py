####################################################################################################################
#
# File:        twitter_stream_kafka.py
# Description: Play the role of kafka producer in the twitter real time stream analytics,
#              after getting the streamed data using twitter api
# Author:      Mostafa Mamdouh
# Created:     Wed May 05 22:17:24 PDT 2021
#
####################################################################################################################


from twitterstreaming import config
from twitterstreaming import twitter_config
from twitterstreaming import twitter_helper
import jsonpickle
import tweepy as tw
from kafka import KafkaProducer


class MyStreamListener(tw.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.producer = KafkaProducer(bootstrap_servers=config.BOOTSTRAP_SERVERS,
                                      key_serializer=lambda screen_name: jsonpickle.encode(screen_name),
                                      value_serializer=lambda tweet: jsonpickle.encode(tweet))

    def on_status(self, tweet):
        topic = config.TOPICS[0]
        self.producer.send(topic=topic, key=tweet.user.screen_name, value=tweet)
        print(tweet)
        print(jsonpickle.encode(tweet))

    def on_error(self, status):
        print("Error detected")
        print(status)


def main():
    # create api object
    api = twitter_helper.Helper().get_api()
    # verify the credentials
    try:
        api.verify_credentials()
        print("You have Successfully Authenticated")
    except Exception as e:
        print("An Error occurred, check the traceback")
        raise e
    # create stream listener that process the stream
    tweets_listener = MyStreamListener(api)
    # create stream object that get the stream
    stream = tw.Stream(api.auth, tweets_listener)
    # filter stream
    stream.filter(track=twitter_config.TRACK, languages=twitter_config.LANGUAGE)


if __name__ == "__main__":
    main()
