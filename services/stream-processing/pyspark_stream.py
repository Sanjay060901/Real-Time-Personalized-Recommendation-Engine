# services/stream-processing/pyspark_stream.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, LongType


spark = SparkSession.builder
.appName('stream_events')
.master('local[*]')
.getOrCreate()


schema = StructType() \
.add('user_id', StringType()) \
.add('product_id', StringType()) \
.add('category', StringType()) \
.add('event_type', StringType()) \
.add('timestamp', LongType())


kafka_df = spark.readStream \
.format('kafka') \
.option('kafka.bootstrap.servers', 'kafka:9092') \
.option('subscribe', 'events') \
.option('startingOffsets', 'earliest') \
.load()


events = kafka_df.selectExpr('CAST(value AS STRING) AS body') \
.select(from_json(col('body'), schema).alias('data')) \
.select('data.*')


# Simple enrichment: map event_type to numeric score
from pyspark.sql.functions import when


events_enriched = events.withColumn('score',
when(col('event_type')=='view', 1)
.when(col('event_type')=='click', 3)
.when(col('event_type')=='add_to_cart', 5)
.when(col('event_type')=='purchase', 10)
.otherwise(0)
)


# Write to delta / parquet (local path for demo)
query = events_enriched.writeStream \
.format('parquet') \
.option('path', '/data/delta/events') \
.option('checkpointLocation', '/data/delta/checkpoints/events') \
.outputMode('append') \
.start()


query.awaitTermination()
