from faker import Faker
from kafka import KafkaProducer
from datetime import datetime
import random
import json

# Inicializar Faker
fake = Faker()

# Configurar Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='192.168.11.10:9094',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Zonas definidas
ZONES = {
    "residential": {"latitude": 40.4168, "longitude": -3.7038, "traffic_factor": 0.5, "fire_probability": 0.1, "industry_factor": 0.2},
    "industrial": {"latitude": 40.4168, "longitude": -3.7178, "traffic_factor": 1.5, "fire_probability": 0.05, "industry_factor": 2.0},
    "center": {"latitude": 40.4198, "longitude": -3.7028, "traffic_factor": 2.0, "fire_probability": 0.15, "industry_factor": 1.0},
    "suburb": {"latitude": 40.4567, "longitude": -3.7314, "traffic_factor": 1.0, "fire_probability": 0.25, "industry_factor": 0.5}
}

# Función para detectar hora punta o fin de semana
def get_traffic_condition(ts):
    dt = datetime.fromisoformat(ts)
    is_weekend = dt.weekday() >= 5
    if not is_weekend and dt.hour in [8, 14, 20]:
        return "peak"
    return "weekend" if is_weekend else "normal"

# Función para generar evento completo
def generate_event():
    city = "Madrid"
    country = "Spain"
    ts = datetime.utcnow().isoformat()
    pollution = {
        "aqius": random.randint(10, 200),
        "mainus": random.choice(["p1", "p2", "p3"])
    }
    traffic = {
        "vehicles_count": random.randint(1000, 7000),
        "vehicles_passed": random.randint(50, 200),
        "industrial_activity": random.choice(["low", "moderate", "high"]),
        "environmental_factors": {
            "fire_active": random.choice([True, False]),
            "fire_intensity": random.choice(["low", "medium", "high"])
        }
    }
    location = {
        "latitude": random.uniform(40.0, 41.0),
        "longitude": random.uniform(-3.7, -3.5)
    }

    # Asignar zona
    zone = random.choice(list(ZONES.values()))
    zone_conditions = {
        "latitude": zone["latitude"],
        "longitude": zone["longitude"],
        "traffic_factor": zone["traffic_factor"],
        "fire_probability": zone["fire_probability"],
        "industry_factor": zone["industry_factor"],
        "vehicles_count": int(random.randint(1000, 7000) * zone["traffic_factor"]),
        "fire_active": random.random() < zone["fire_probability"],
        "industrial_activity": "high" if zone["industry_factor"] > 1 else ("moderate" if zone["industry_factor"] == 1 else "low")
    }

    # Determinar condición de tráfico
    traffic_condition = get_traffic_condition(ts)

    # Calcular AQI actualizado
    aqi = pollution["aqius"]
    if traffic_condition == "peak":
        aqi += random.randint(20, 60)
    elif traffic_condition == "weekend" and zone_conditions["fire_active"]:
        aqi += 100 if traffic["environmental_factors"]["fire_intensity"] == "high" else 50
    if zone_conditions["fire_active"]:
        aqi += 50 if traffic["environmental_factors"]["fire_intensity"] == "low" else 100

    event = {
        "city": city,
        "country": country,
        "ts": ts,
        "pollution": pollution,
        "traffic": traffic,
        "location": location,
        "zone_conditions": zone_conditions,
        "traffic_condition": traffic_condition,
        "updated_aqi": aqi
    }

    return event

# Enviar datos en bucle
def main():
    while True:
        event = generate_event()
        producer.send("air_quality_topic", value=event)
        print("✅ Sent to Kafka:", event)
        producer.flush()
        # Esperar 1 segundo entre envíos
        import time
        time.sleep(1)

if __name__ == "__main__":
    main()
