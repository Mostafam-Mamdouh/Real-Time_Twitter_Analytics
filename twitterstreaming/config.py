####################################################################################################################
#
# File:        config.py
# Description: A config file, for Kafka, Spark, NLP. It contains topics, partitions,
#              offsets to start from them, HDFS path, and some other things.
# Author:      Mostafa Mamdouh
# Created:     Wed May 05 22:17:24 PDT 2021
#
####################################################################################################################



# =================== Kafka config =================== #
# BOOTSTRAP_SERVERS = "localhost:9092"
BOOTSTRAP_SERVERS = "sandbox-hdp.hortonworks.com:6667"
KAFKA_PARAMS = {"metadata.broker.list": BOOTSTRAP_SERVERS}

# KAFKA_PARAMS["auto.offset.reset"] = "latest" # earliest if you want
# KAFKA_PARAMS["enable.auto.commit"] = "false"
TOPICS = ["twitter"]
# dict contains info about topic, and corresponding partitions, offsets
# twitter is topic, [partition, offset] = [0, 0]
TOPICS_PARTIONS_OFFSETS = {TOPICS[0]: [0, 0]}

# =================== Spark config =================== #
# path for parquet file
PARQUET_PATH = r"hdfs:///tmp/big_data/Twitter/tweets_stg/tweets_stg.parquet"
# path of checkpoint for the last consumed offset object
OFFSET_FILE_PATH = r"twitterstreaming/offset.pkl"
# path of check point
CHECKPOINT = r'.'

# =================== NLP config =================== #
POSITIVE = "This is a Positive one."
NEGATIVE = "This is a Negative one."
NEUTRAL = "This is a Neutral one."
