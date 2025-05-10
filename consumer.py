from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, BooleanType
import pandas as pd

# Esquema actualizado según la estructura del evento
schema = StructType([
    StructField("city", StringType(), True),
    StructField("country", StringType(), True),
    StructField("ts", StringType(), True),
    StructField("pollution", StructType([
        StructField("aqius", IntegerType(), True),
        StructField("mainus", StringType(), True)
    ])),
    StructField("traffic", StructType([
        StructField("vehicles_count", IntegerType(), True),
        StructField("vehicles_passed", IntegerType(), True),
        StructField("industrial_activity", StringType(), True),
        StructField("environmental_factors", StructType([
            StructField("fire_active", BooleanType(), True),
            StructField("fire_intensity", StringType(), True)
        ]))
    ])),
    StructField("location", StructType([
        StructField("latitude", FloatType(), True),
        StructField("longitude", FloatType(), True)
    ])),
    StructField("zone_conditions", StructType([
        StructField("zone", StringType(), True),
        StructField("latitude", FloatType(), True),
        StructField("longitude", FloatType(), True),
        StructField("traffic_factor", FloatType(), True),
        StructField("fire_probability", FloatType(), True),
        StructField("industry_factor", FloatType(), True),
        StructField("vehicles_count", IntegerType(), True),
        StructField("fire_active", BooleanType(), True),
        StructField("industrial_activity", StringType(), True)
    ])),
    StructField("traffic_condition", StringType(), True),
    StructField("updated_aqi", IntegerType(), True)
])

# Crear sesión de Spark
spark = SparkSession.builder \
    .appName("KafkaAirQualityConsumer") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Leer desde Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.11.10:9094") \
    .option("subscribe", "air_quality") \
    .option("startingOffsets", "earliest")
    .load()

# Parsear JSON
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Crear un DataFrame acumulativo vacío para almacenar las alertas de contaminación
accumulated_schema = StructType([
    StructField("city", StringType(), True),
    StructField("alert", StringType(), True),
    StructField("timestamp", StringType(), True)
])

accumulated_df = spark.createDataFrame([], accumulated_schema)

# Función para procesar cada lote de datos
def process_batch(batch_df, epoch_id):
    global accumulated_df  # Utilizar el DataFrame acumulativo global

    # Convertir a Pandas DataFrame para poder procesar fácilmente
    pd_df = batch_df.toPandas()

    if not pd_df.empty:
        # Añadir columna de alerta
        pd_df['alert'] = pd_df['updated_aqi'].apply(lambda x: 'HIGH POLLUTION' if x > 100 else 'OK')

        print(f"\n=== Lote {epoch_id} ===")
        print(pd_df[['city', 'ts', 'updated_aqi', 'alert']].head(10))

        # Filtrar alertas de alta contaminación
        high_alerts = pd_df[pd_df['alert'] == 'HIGH POLLUTION']
        if not high_alerts.empty:
            print("ALERTAS DE ALTA CONTAMINACIÓN:")
            print(high_alerts[['city', 'ts', 'updated_aqi', 'zone_conditions', 'traffic_condition']].to_string(index=False))
        
        # Convertir las alertas filtradas en un DataFrame de Spark
        high_alerts_spark_df = spark.createDataFrame(high_alerts[['city', 'alert', 'ts']])

        # Acumular las alertas de alta contaminación
        accumulated_df = accumulated_df.union(high_alerts_spark_df)

        # Mostrar el DataFrame acumulativo hasta ahora
        accumulated_df.show()

    try:
        # Guardar el DataFrame original en HDFS (en formato Parquet)
        batch_df.write \
            .mode("append") \
            .parquet("hdfs://cluster-bda:9000/opt/kafka/proyecto_MLU/data/")
        print("Datos escritos en HDFS correctamente.")
    except Exception as e:
        print(f"Error escribiendo en HDFS: {e}")

# Ejecutar stream
query = parsed_df \
    .writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

# Esperar a que termine el streaming
query.awaitTermination()
