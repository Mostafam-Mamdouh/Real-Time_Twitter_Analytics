####################################################################################################################
#
# File:        schema.py
# Description: Spark schema definition for the data frame to be written as parquet file on HDFS
# Author:      Mostafa Mamdouh
# Created:     Wed May 05 22:17:24 PDT 2021
#
####################################################################################################################


import findspark

try:
    findspark.init()
except ValueError:
    pass

from pyspark.sql.types import StructType, StructField, StringType, FloatType, LongType, TimestampType, DateType


# Spark Schema
'''
# fields of interest (see get_fields function in stream_handler_proessed.py/stream_handler.py)
fields = [tweet.id_str, tweet.timestamp_ms, tweet.created_at,
          tweet.user.id_str, tweet.user.screen_name, tweet.user.name,
          tweet.user.location, tweet.user.followers_count, tweet.text,
          score, msg_to_send]
'''
# note, types will be the same as the types in tweet object except uni will be converted to string
SCHEMA = StructType([
            StructField("tweet_id", StringType(), True),
            StructField("tweet_timestamp_ms", TimestampType(), True),
            StructField("tweet_created_at", DateType(), True),
            StructField("id", StringType(), True),
            StructField("screen_name", StringType(), True),
            StructField("name", StringType(), True),
            StructField("location", StringType(), True),
            StructField("followers_count", LongType(), True),
            StructField("msg", StringType(), True),
            StructField("score", FloatType(), True),
            StructField("msg_to_send", StringType(), True)
        ])

