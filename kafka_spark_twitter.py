####################################################################################################################
#
# File:        kafka_spark_twitter.py
# Description: Play the role of kafka consumer in the twitter real time stream analytics, and connect kafka
#              to spark to start the the main processing, use this file if you want to consume from earliest,
#              or latest, and add the corrosponding configuration in the config.py
# Author:      Mostafa Mamdouh
# Created:     Wed May 05 22:17:24 PDT 2021
#
####################################################################################################################


from twitterstreaming import config
from twitterstreaming import stream_handler
import jsonpickle
import findspark

try:
    findspark.init()
except ValueError:
    pass

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
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
    stream_process = stream_handler.StreamHandler()

    # kafka consumer-spark connection
    kafka_stream = KafkaUtils.createDirectStream(ssc, config.TOPICS,
                                                 kafkaParams=config.KAFKA_PARAMS,
                                                 keyDecoder=lambda screen_name: jsonpickle.encode(screen_name),
                                                 valueDecoder=lambda tweet: jsonpickle.decode(tweet))

    # process the stream
    kafka_stream.foreachRDD(lambda rdd: stream_process.process(rdd, spark))
    # ssc.checkpoint(r'/home/big_data')
    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
