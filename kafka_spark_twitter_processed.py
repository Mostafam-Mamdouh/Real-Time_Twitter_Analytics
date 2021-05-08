####################################################################################################################
#
# File:        kafka_spark_twitter_processed.py
# Description: Same as kafka_spark_twitter.py, but it keeps tracking offsets, and persist them in disk, to make sure
#              that all the data in the topic is consumed by spark, use kafka_spark_twitter.py file if you want to 
#              consume from earliest, or latest, and add the corrosponding configuration in the config.py
# Author:      Mostafa Mamdouh
# Created:     Wed May 05 22:17:24 PDT 2021
#
####################################################################################################################


from twitterstreaming import config
from twitterstreaming import stream_handler_proessed
import jsonpickle
import findspark

try:
    findspark.init()
except ValueError:
    pass

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark.sql import SparkSession


def spark_context_creator():
    # create SC with the specified configuration
    conf = SparkConf()
    conf.setAppName("kafka-spark-twitter")
    sc = SparkContext(conf=conf)
    return(sc)


def main():
    # create spark context, spark session
    sc = spark_context_creator()
    spark = SparkSession(sc)
    # To avoid unnecessary logs
    sc.setLogLevel("WARN")
    # create streaming context
    ssc = StreamingContext(sc, 3)

    # create stream handler object to process stream
    stream_process = stream_handler_proessed.StreamHandler()

    # prepare direct stream parameters
    kafka_params = config.KAFKA_PARAMS
    # checkpoint for the last consumed offset object
    offset_file_path = config.OFFSET_FILE_PATH
    # get last consumed offset
    offset_ranges = stream_process.get_offset(offset_file_path)
    topics = []
    from_offset = {}
    # if list empty, means first time to consume, then configure manually
    if (not offset_ranges):
        topics = list(config.TOPICS_PARTIONS_OFFSETS.keys())
        topics_partions_offsets = config.TOPICS_PARTIONS_OFFSETS
        for topic in list(topics_partions_offsets.keys()):
            topic_partion = TopicAndPartition(topic, topics_partions_offsets[topic][0])
            from_offset[topic_partion] = topics_partions_offsets[topic][1]
    # get info from saved offset_ranges object
    else:
        for o in offset_ranges:
            topics.append(o.topic)
            topic_partion = TopicAndPartition(o.topic, o.partition)
            from_offset[topic_partion] = o.untilOffset

    # kafka consumer-spark connection
    kafka_direct_stream = KafkaUtils.createDirectStream(ssc, topics=topics, kafkaParams=kafka_params, fromOffsets=from_offset,
                                                        keyDecoder=lambda screen_name: jsonpickle.encode(screen_name),
                                                        valueDecoder=lambda tweet: jsonpickle.decode(tweet))

    # process the stream
    kafka_direct_stream.foreachRDD(lambda rdd: stream_process.process(rdd, spark, offset_file_path))
    # ssc.checkpoint(config.CHECKPOINT)
    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
