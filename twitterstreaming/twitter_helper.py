####################################################################################################################
#
# File:        twitter_helper.py
# Description: A helper file that create twitter api object, and can retweet
# Author:      Mostafa Mamdouh
# Created:     Wed May 05 22:17:24 PDT 2021
#
####################################################################################################################


import twitter_config
import datetime
import tweepy as tw


# twitter Helper class
class Helper(object):
    def __init__(self):
        # Authenticate to Twitter
        self.auth = tw.OAuthHandler(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET)
        self.auth.set_access_token(twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
        # Create API object
        self.api = tw.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # getter for api
    def get_api(self):
        return(self.api)

    # method to retweet
    def retweet(self, tweet_id, screen_name, name, msg_to_send):
        # send retweet
        time_stamp = str(datetime.datetime.now())
        #self.api.update_status("Hello Mr/Ms " + name + ", " +  msg_to_send + " @" + screen_name +
        #                        "\n" + "This message sent at " + time_stamp, tweet_id)
