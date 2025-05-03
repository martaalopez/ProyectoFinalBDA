from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf, current_timestamp, hour
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, BooleanType
from faker import Faker
import random
import pandas as pd
import numpy as np
import datetime

# Definir el esquema de los datos
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
        StructField("vehicles_passed", IntegerType(), True),  # Nuevo campo para contar los coches
        StructField("industrial_activity", StringType(), True),
        StructField("environmental_factors", StructType([
            StructField("fire_active", BooleanType(), True),
            StructField("fire_intensity", StringType(), True)
        ]))
    ])),
    StructField("location", StructType([
        StructField("latitude", FloatType(), True),
        StructField("longitude", FloatType(), True)
    ]))
])

# Crear sesión de Spark
spark = SparkSession.builder \
    .appName("AirQualityDataProcessor") \
    .getOrCreate()

# Instanciar Faker
fake = Faker()

# Generar datos sintéticos con Faker
def generate_synthetic_data():
    # Generar datos aleatorios para una ciudad y país
    city = fake.city()
    country = fake.country()

    # Generar fecha en formato ISO
    ts = fake.date_time_this_year().isoformat()

    # Generar datos de contaminación
    aqius = random.randint(10, 200)  # Valor de AQI aleatorio
    mainus = random.choice(["p1", "p2", "p3"])  # Tipo de contaminante principal

    # Generar datos de tráfico
    vehicles_count = random.randint(1000, 7000)  # Número de vehículos
    vehicles_passed = random.randint(50, 200)  # Número de vehículos que pasan en el intervalo de tiempo (por ejemplo, 1 segundo)
    industrial_activity = random.choice(["low", "moderate", "high"])  # Actividad industrial
    fire_active = random.choice([True, False])  # Incendio activo o no
    fire_intensity = random.choice(["low", "medium", "high"]) if fire_active else "none"  # Intensidad del incendio

    # Generar latitud y longitud
    latitude = random.uniform(40.0, 41.0)  # Rango de latitudes para Madrid
    longitude = random.uniform(-3.7, -3.5)  # Rango de longitudes para Madrid

    # Devolver los datos generados
    return {
        "city": city,
        "country": country,
        "ts": ts,
        "pollution": {
            "aqius": aqius,
            "mainus": mainus
        },
        "traffic": {
            "vehicles_count": vehicles_count,
            "vehicles_passed": vehicles_passed,  # Guardamos los coches que pasaron en el evento
            "industrial_activity": industrial_activity,
            "environmental_factors": {
                "fire_active": fire_active,
                "fire_intensity": fire_intensity
            }
        },
        "location": {
            "latitude": latitude,
            "longitude": longitude
        }
    }

# Crear el DataFrame con los datos sintéticos
synthetic_data = [generate_synthetic_data() for _ in range(1000)]  # Generamos 1000 eventos sintéticos

# Crear un DataFrame a partir de los datos sintéticos
synthetic_df = spark.createDataFrame(synthetic_data, schema)

# Asignar zona y condiciones específicas según la ciudad y la zona
def assign_zone_and_conditions(city):
    # Definir las zonas de Madrid
    zones = {
        "residential": {"latitude": 40.4168, "longitude": -3.7038, "traffic_factor": 0.5, "fire_probability": 0.1, "industry_factor": 0.2},  # Menos tráfico, menos industria
        "industrial": {"latitude": 40.4168, "longitude": -3.7178, "traffic_factor": 1.5, "fire_probability": 0.05, "industry_factor": 2.0},  # Más tráfico, más industria
        "center": {"latitude": 40.4198, "longitude": -3.7028, "traffic_factor": 2.0, "fire_probability": 0.15, "industry_factor": 1.0},  # Mucho tráfico, más contaminación
        "suburb": {"latitude": 40.4567, "longitude": -3.7314, "traffic_factor": 1.0, "fire_probability": 0.25, "industry_factor": 0.5}  # Moderado tráfico, más incendios
    }

    zone = random.choice(list(zones.values()))  # Elegir aleatoriamente una zona

    # Modificar los datos de tráfico, industria y contaminación en función de la zona
    if city == "Madrid":
        # Ajustar los factores de tráfico, incendio y actividad industrial según la zona
        zone['vehicles_count'] = random.randint(1000, 7000) * zone["traffic_factor"]
        zone['fire_active'] = random.random() < zone["fire_probability"]
        zone['industrial_activity'] = "moderate" if zone["industry_factor"] == 1 else "high" if zone["industry_factor"] > 1 else "low"
    return zone

# Registrar la UDF para asignar la zona y condiciones
assign_zone_udf = udf(assign_zone_and_conditions, StructType([
    StructField("latitude", FloatType(), True),
    StructField("longitude", FloatType(), True),
    StructField("traffic_factor", FloatType(), True),
    StructField("fire_probability", FloatType(), True),
    StructField("industry_factor", FloatType(), True),
    StructField("vehicles_count", IntegerType(), True),
    StructField("fire_active", BooleanType(), True),
    StructField("industrial_activity", StringType(), True)
]))

# Aplicar la asignación de zona
updated_df = synthetic_df.withColumn("zone_conditions", assign_zone_udf(synthetic_df["city"]))

# Función para identificar si es hora punta o fin de semana
def is_peak_or_weekend(ts):
    dt = datetime.datetime.fromisoformat(ts)
    # Verificar si es un fin de semana
    is_weekend = dt.weekday() >= 5  # 5 y 6 son sábado y domingo
    hour_of_day = dt.hour

    # Verificar si es hora punta (Lunes a viernes)
    if not is_weekend:
        if hour_of_day in [8, 14, 20]:  # 08:00-09:00, 14:00-15:00, 20:00-21:00
            return "peak"
    return "normal" if not is_weekend else "weekend"

# Registrar la UDF para identificar la hora punta o fin de semana
is_peak_or_weekend_udf = udf(is_peak_or_weekend, StringType())

# Aplicar la UDF para identificar la hora punta o fin de semana
updated_df = updated_df.withColumn("traffic_condition", is_peak_or_weekend_udf(updated_df["ts"]))

# Definir una función para actualizar el AQI
def update_aqi(row):
    aqi = row['pollution']['aqius']
    vehicles_count = row['zone_conditions']['vehicles_count']
    fire_active = row['zone_conditions']['fire_active']
    fire_intensity = row['traffic']['environmental_factors']['fire_intensity']
    traffic_condition = row['traffic_condition']

    # Si es hora punta o hay más tráfico, el AQI aumenta
    if traffic_condition == "peak":
        aqi += random.randint(20, 60)  # Aumento por tráfico en hora punta
    elif traffic_condition == "weekend" and fire_active:
        # Más incendios en fin de semana, el AQI empeora mucho si hay incendio
        aqi += 100 if fire_intensity == "high" else 50
    
    # Si hay un incendio activo, el AQI empeora considerablemente
    if fire_active:
        aqi += 50 if fire_intensity == "low" else 100  # El impacto del incendio en el AQI

    return aqi

# Registrar la UDF para actualizar el AQI
update_aqi_udf = udf(update_aqi, IntegerType())

# Aplicar la UDF para actualizar el AQI
updated_df = updated_df.withColumn("updated_aqi", update_aqi_udf(updated_df))

# Procesar los datos en batch
def process_batch(df, epoch_id):
    # Convertir a Pandas DataFrame
    pd_df = df.toPandas()

    # Procesar el histórico de contaminación y alertas
    if not pd_df.empty:
        pd_df['alert'] = np.where(pd_df['updated_aqi'] > 100, 'High Pollution', 'Normal')

        # Mostrar el resultado procesado
        print("Batch Result:")
        print(pd_df.head())

# Escribir el flujo en batch
query = updated_df \
    .writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

query.awaitTermination()
