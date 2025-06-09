from kafka import KafkaProducer
from datetime import datetime, timedelta
import random
import json
import time
from sqlalchemy import create_engine # SQLAlchemy + pandas: conectarse y leer de MySQL.
import pandas as pd


# Configurar el productor de Kafka
# Se conecta al servidor Kafka y define que los mensajes enviados serán serializados como JSON.
producer = KafkaProducer(
    bootstrap_servers='192.168.11.10:9094',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
 
# Creamos la  conexión a MySQL
mysql_engine = create_engine("mysql+pymysql://marta:marta@localhost:3306/kafka_air_quality")

# Obtenemos el  último timestamp ,si no hay, empieza desde 2 de enero de 2025, 9:00 AM.
def get_last_timestamp():
    try:
        query = "SELECT MAX(ts) as last_ts FROM air_quality_events"
        df = pd.read_sql(query, con=mysql_engine)
        ts = df["last_ts"].iloc[0]
        if pd.notnull(ts):
            return pd.to_datetime(ts).to_pydatetime()
    except Exception as e:
        print("Error al obtener ts desde MySQL:", e)
    # Si no hay ts válido, empezar desde aquí
    return datetime(2025, 1, 2, 9, 0, 0)


ZONE_STATE = {}

ZONES = {
    "residential": {"latitude": 40.519799, "longitude": -3.633613, "traffic_factor": 0.5, "fire_probability": 0.05, "industry_factor": 0.1, "vehicle_rate": 0.05},
    "industrial":  {"latitude": 40.348246, "longitude": -3.799463, "traffic_factor": 1.5, "fire_probability": 0.01, "industry_factor": 2.0, "vehicle_rate": 0.2},
    "center":      {"latitude": 40.419285, "longitude": -3.696985, "traffic_factor": 2.5, "fire_probability": 0.01, "industry_factor": 0.3, "vehicle_rate": 0.3},
    "suburb":      {"latitude": 40.613517, "longitude": -3.848663, "traffic_factor": 0.1, "fire_probability": 0.3, "industry_factor": 0.0, "vehicle_rate": 0.01},
}

#Estado inicial de cada zona
for zone in ZONES:
    ZONE_STATE[zone] = {
        "aqi": random.randint(30, 60),
        "fire_active": False,
        "fire_end_time": None,
        "fire_intensity": None,
        "vehicles_count": 0
    }

SPECIAL_EVENTS = [
    {
        "name": "concert",
        "start": datetime(2025, 1, 3, 18, 0),
        "end": datetime(2025, 1, 3, 19, 0)
    },
    {
        "name": "football_match",
        "start": datetime(2025, 1, 4, 20, 0),
        "end": datetime(2025, 1, 4, 21, 0)
    }
]



SIM_TIME = get_last_timestamp()
SIM_STEP = timedelta(minutes=5)  # Cada segundo real simula 5 minutos
REAL_SLEEP_TIME = 1  # 1 segundo real = 5 minutos simulados


def check_special_event(sim_time):
    for event in SPECIAL_EVENTS:
        if event["start"] <= sim_time < event["end"]:
            return event["name"]
    return None


# Determina si es hora pico:
def get_traffic_condition(sim_dt):
    is_weekend = sim_dt.weekday() >= 5
    peak_hours = [8, 9, 14, 15, 20]
    return "peak" if not is_weekend and sim_dt.hour in peak_hours else "weekend" if is_weekend else "normal"

# Generación de un evento
def generate_event(zone_name, zone, sim_time):
    state = ZONE_STATE[zone_name]
    ts = sim_time.isoformat()
    condition = get_traffic_condition(sim_time)

    if zone_name == "center":
        vehicles_passed = random.randint(30, 50) if condition == "peak" else random.randint(10, 20)
    elif zone_name == "industrial":
        vehicles_passed = random.randint(20, 40) if condition == "peak" else random.randint(10, 20)
    elif zone_name == "residential":
        vehicles_passed = random.randint(10, 15) if condition == "peak" else random.randint(5, 10)
    else:  # suburb
        vehicles_passed = random.randint(1, 5)

    # Actualiza el número de vehículos en circulación en una zona,simulando que el 10% se va y se suman los nuevos que acaban de pasar
    state["vehicles_count"] = int(state["vehicles_count"] * 0.9) + vehicles_passed

    # Activa un incendio aleatoriamente según la probabilidad de la zona y lo desactiva automáticamente tras dos horas simuladas.
    if not state["fire_active"] and random.random() < zone["fire_probability"]:
        state["fire_active"] = True
        state["fire_end_time"] = sim_time + timedelta(hours=2)
        state["fire_intensity"] = random.choice(["low", "medium", "high"])
    elif state["fire_active"] and sim_time >= state["fire_end_time"]:
        state["fire_active"] = False
        state["fire_end_time"] = None
        state["fire_intensity"] = None

#  Se simula que el tráfico aumenta porque muchas personas van al evento.
    special_event = check_special_event(sim_time) if zone_name == "center" else None
    if special_event:
        state["vehicles_count"] += random.randint(30, 50)

    aqi = state["aqi"]
    delta = 0

    # Cada vehículo aporta un 2% al aumento de AQI.
    delta += int(state["vehicles_count"] * 0.02)

    # Si es hora pico,se añade un incremento fijo de 10 al AQI.
    if condition == "peak":
        delta += 10

    # Si hay un incendio,se suma contaminación dependiendo de su intensidad.
    if state["fire_active"]:
        delta += {"low": 5, "medium": 10, "high": 20}[state["fire_intensity"]]
    else:
    #Si no hay incendio,se reduce ligeramente el AQI 
        delta -= 2

    # Factor industrial solo si aplica por hora y zona
    if zone_name == "industrial" and sim_time.hour in [9, 10, 11, 12]:
        delta += random.randint(30, 50)
    elif zone_name in ["residential", "center"]:
        delta += int(zone["industry_factor"] * 5)

    # Evento especial
    if special_event:
        delta += 10

    # Accidentes.Hay una pequeña probabilidad de accidente:1% en el centro.0.3% en otras zonas.Un accidente aumenta la contaminación en 15 unidades.
    if random.random() < (0.01 if zone_name == "center" else 0.003):
        delta += 15

    # AQI final,se suma delta al AQI actual.
    new_aqi = max(10, min(200, aqi + delta))

    # Normalizar según zona
    if zone_name == "suburb":
        if state["fire_active"]:
            new_aqi = min(max(new_aqi, 50), 100)
        else:
            new_aqi = min(new_aqi, 50)

    elif zone_name == "residential":
        new_aqi = min(new_aqi, 100)

    elif zone_name == "industrial":
        if sim_time.hour in [9, 10, 11, 12]:
            new_aqi = min(max(new_aqi, 150), 200)
        else:
            new_aqi = min(max(new_aqi, 101), 150)

    elif zone_name == "center":
        if condition == "peak":
            new_aqi = min(max(new_aqi, 150), 200)
        else:
            new_aqi = min(max(new_aqi, 101), 150)

    state["aqi"] = new_aqi

        # Aplicar condiciones de fin de semana
    if sim_time.weekday() >= 5:  # 5=sábado, 6=domingo
        if zone_name == "center":
            new_aqi = min(max(new_aqi, 100), 115)
        elif zone_name == "industrial":
            new_aqi = min(max(new_aqi, 50), 100)



    return {
        "city": "Madrid",
        "country": "Spain",
        "ts": ts,
        "pollution_aqius": new_aqi,
        "pollution_mainus": random.choice(["p1", "p2", "p3"]),
        "vehicles_count": state["vehicles_count"],
        "vehicles_passed": vehicles_passed,
        "industrial_activity": "high" if zone["industry_factor"] > 1 else "moderate" if zone["industry_factor"] > 0 else "low",
        "fire_active": state["fire_active"],
        "fire_intensity": state["fire_intensity"] if state["fire_active"] else "none",
        "accident": "yes" if random.random() < 0.01 else "no",
        "latitude": zone["latitude"],
        "longitude": zone["longitude"],
        "zone": zone_name,
        "traffic_factor": zone["traffic_factor"],
        "fire_probability": zone["fire_probability"],
        "industry_factor": zone["industry_factor"],
        "traffic_condition": condition,
        "special_event": special_event if special_event else "none",
    }

def main():
    global SIM_TIME
    while True:
        if SIM_TIME.hour >= 9:
            for zone_name, zone in ZONES.items():
                event = generate_event(zone_name, zone, SIM_TIME)
                producer.send("air-quality", value=event)
                print(event)

            producer.flush()
        SIM_TIME += SIM_STEP
        time.sleep(REAL_SLEEP_TIME)

if __name__ == "__main__":
    main()

