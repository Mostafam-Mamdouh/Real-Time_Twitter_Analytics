# Real-Time_Twitter_Analytics

A Big Data Solution end to end pipeline for Real-Time_Twitter_Analytics.
See below architecture for the full pipeline.


## Architecture

![Architecture](https://github.com/Mostafam-Mamdouh/Real-Time_Twitter_Analytics/blob/master/images/Architecture.png?raw=true)


## Visualizations

![Visualization_1](https://github.com/Mostafam-Mamdouh/Real-Time_Twitter_Analytics/blob/master/images/Visualization_1.png?raw=true)
![Visualization_2](https://github.com/Mostafam-Mamdouh/Real-Time_Twitter_Analytics/blob/master/images/Visualization_2.png?raw=true)


## Installation

See installation_guide, it contains steps.txt, and requirements.txt


## Usage

- Run twitter_stream_kafka.py, to get streams from Twitter API, and act as producer for Kafka.

- Run kafka_spark_twitter_processed.py/kafka_spark_twitter.py, to act as consumer for Kafka to consume tweets, analyze them, apply sentiment analysis, write to HDFS as parquet file, and then retweet.

- Run ambari_service_monitoring.py, if you want to monitor services, using Ambari REST API.

- Use kafka_spark_twitter.py, if you want to consume from latest, or earliest.

- Use kafka_spark_twitter_processed.py, if you want to keep track offsets, and persist them in disk, to make sure that all the data in the topic is consumed by spark.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
