from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, BooleanType
import pandas as pd

# Definir el esquema completo del JSON producido
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

# Leer el flujo de datos desde Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.11.10:9094") \
    .option("subscribe", "air_quality_topic") \
    .option("startingOffsets", "latest") \
    .load()

# Parsear el valor como JSON
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Definir el procesamiento de cada microbatch
def process_batch(batch_df, epoch_id):
    pd_df = batch_df.toPandas()

    if not pd_df.empty:
        # Agregar columna de alerta: "HIGH POLLUTION" si el AQI actualizado es mayor a 100, de lo contrario 'OK'
        pd_df['alert'] = pd_df['updated_aqi'].apply(lambda x: 'HIGH POLLUTION' if x > 100 else 'OK')

        # Mostrar resumen del lote procesado
        print(f"\n=== Lote {epoch_id} ===")
        print(pd_df[['city', 'ts', 'updated_aqi', 'alert']].head(10))

        # Filtrar las alertas de alta contaminación
        high_alerts = pd_df[pd_df['alert'] == 'HIGH POLLUTION']
        if not high_alerts.empty:
            print("ALERTAS DE ALTA CONTAMINACIÓN:")
            print(high_alerts[['city', 'ts', 'updated_aqi']].to_string(index=False))

# Ejecutar el stream con foreachBatch para procesar los datos en microbatches
query = parsed_df \
    .writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

# Esperar a que termine la consulta
query.awaitTermination()

