####################################################################################################################
#
# File:        stream_handler.py
# Description: A file that handle the twitter real time stream analytics, and do the main processing job,
#              like sentiment analysis, prepare the schema, and writing parquet file to hdfs. This file is used
#              by kafka_spark_twitter_processed.py
# Author:      Mostafa Mamdouh
# Created:     Wed May 05 22:17:24 PDT 2021
#
####################################################################################################################

import config
import schema
import twitter_helper
import datetime
import unicodedata
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class StreamHandler(object):
    def __init__(self):
        # define helper object to use it, to retweet
        self.sender = twitter_helper.Helper()
        # define schema according to the fields of interest
        # note, types will be the same as the types in tweet object except uni will be converted to string
        self.schema = schema.SCHEMA

    # writing parquet file to hdfs
    def write_parquet(self, df):
        print("write parquet to hdfs")
        df.coalesce(1).write.mode('append').parquet(config.PARQUET_PATH)

    # from epoch to timestamp in ms
    def epoch_to_ts(self, epoch):
        str_epoch = epoch[:-3] + '.' + epoch[-3:]
        return (datetime.datetime.fromtimestamp(float(str_epoch)))

    # from uni to str
    def uni_to_str(self, uni):
        return (unicodedata.normalize('NFKD', uni).encode('ascii', 'ignore'))

    # get fields of interest
    def get_fields(self, tweet):
        # apply sentiment analysis
        score, msg_to_send = self.sentiment_analysis(tweet.text)
        # get fields of interest
        fields = [tweet.id_str, tweet.timestamp_ms, tweet.created_at,
                  tweet.user.id_str, tweet.user.screen_name, tweet.user.name,
                  tweet.user.location, tweet.user.followers_count, tweet.text,
                  score, msg_to_send]
        # convert uni fields only to string
        for i, field in enumerate(fields):
            if (type(field) == unicode):
                fields[i] = self.uni_to_str(field)
        # Epoch timestamp from string to float or timestamp
        fields[1] = self.epoch_to_ts(fields[1])
        return(fields)

    # apply sentiment analysis
    def sentiment_analysis(self, text):
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(text)
        comp_score = score["compound"]
        if (comp_score >= 0.05):
            msg_to_send = config.POSITIVE
        elif (comp_score <= -0.05):
            msg_to_send = config.NEGATIVE
        else:  # (comp_score > -0.05) and (comp_score < 0.05)
            msg_to_send = config.NEUTRAL
        return (comp_score, msg_to_send)

    # perform the logic on the records
    def logic(self, record):
        tweet = record[1]  # take only value without key
        # get fields of interest
        fields = self.get_fields(tweet)
        return (fields)

    # the main method that handle the stream, and call other methods
    def process(self, rdd, spark):
        # get desired fields
        rdd_fields = rdd.map(self.logic)
        # mark an RDD to be persisted in memory, as long as the right storage level is provided
        rdd_fields.cache()
        # if rdd is not empty (the batch is not empty)
        if (not rdd_fields.isEmpty()):
            # convert rdd to data frame, to write to parquet
            df = spark.createDataFrame(rdd_fields, self.schema)
            df.show(truncate=50)
            # write as parquet to hdfs
            self.write_parquet(df)
            # retweet, take necessary cols, tweet_id, screen_name, name, msg_to_send
            rdd_fields.foreach(lambda record: self.sender.retweet(tweet_id=record[0], screen_name=record[4],
                                                                  name=record[5], msg_to_send=record[-1]))


