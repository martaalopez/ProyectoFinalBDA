from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, BooleanType
import pandas as pd
from sqlalchemy import create_engine
from pyspark.sql.types import TimestampType

# Configuración para la conexión a MySQL 
mysql_engine = create_engine("mysql+pymysql://marta:marta@localhost:3306/kafka_air_quality")

# Crear sesión de Spark
spark = SparkSession.builder \
    .appName("KafkaAirQualityConsumer") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://cluster-bda:9000") \
    .getOrCreate()

# Definir esquema del JSON que llega de Kafka
schema = StructType([
    StructField("city", StringType(), True),
    StructField("country", StringType(), True),
    StructField("ts", TimestampType(), True),
    StructField("pollution_aqius", IntegerType(), True),
    StructField("pollution_mainus", StringType(), True),
    StructField("vehicles_count", IntegerType(), True),
    StructField("vehicles_passed", IntegerType(), True),
    StructField("industrial_activity", StringType(), True),
    StructField("fire_active", BooleanType(), True),
    StructField("fire_intensity", StringType(), True),
    StructField("latitude", FloatType(), True),
    StructField("longitude", FloatType(), True),
    StructField("zone", StringType(), True),
    StructField("traffic_factor", FloatType(), True),
    StructField("fire_probability", FloatType(), True),
    StructField("industry_factor", FloatType(), True),
    StructField("traffic_condition", StringType(), True),
    StructField("special_event", StringType(), True),
])

spark.sparkContext.setLogLevel("ERROR")

# Leer stream de Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.11.10:9094") \
    .option("subscribe", "air-quality") \
    .option("startingOffsets", "latest") \
    .load()

# Parsear JSON
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

def process_batch(batch_df, epoch_id):
    # Convertir batch de Spark a Pandas
    pd_df = batch_df.toPandas()

    if not pd_df.empty:
        # Aquí solo imprimimos datos
        print(f"\n=== Lote {epoch_id} ===")
        print(pd_df[['city', 'country', 'ts', 'pollution_aqius']].head(10))

        # Guardar todos los datos que vienen en el DataFrame 
        pd_df.to_sql('air_quality_events', con=mysql_engine, if_exists='append', index=False)

    # Guardar batch en parquet en HDFS 
    batch_df.write \
        .format("parquet") \
        .mode("append") \
        .option("compression", "snappy") \
        .save("hdfs://cluster-bda:9000/opt/kafka/proyecto_MLU/data/")


# Ejecutar streaming con foreachBatch para procesamiento personalizado
query = parsed_df.writeStream \
    .outputMode("append") \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()

