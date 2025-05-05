from kafka import KafkaProducer
from datetime import datetime
import random
import json
import time

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='192.168.11.10:9094',  # Dirección del broker de Kafka
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializa los mensajes como JSON
)

# Definición de las zonas con sus características geográficas y de contaminación
ZONES = {
    "residential": {
        "latitude": 40.4168, "longitude": -3.7038,
        "traffic_factor": 0.5, "fire_probability": 0.1, "industry_factor": 0.2
    },
    "industrial": {
        "latitude": 40.4168, "longitude": -3.7178,
        "traffic_factor": 1.5, "fire_probability": 0.05, "industry_factor": 2.0
    },
    "center": {
        "latitude": 40.4198, "longitude": -3.7028,
        "traffic_factor": 2.0, "fire_probability": 0.15, "industry_factor": 1.0
    },
    "suburb": {
        "latitude": 40.4567, "longitude": -3.7314,
        "traffic_factor": 1.0, "fire_probability": 0.25, "industry_factor": 0.5
    }
}

# Función para detectar si es hora punta o fin de semana
def get_traffic_condition(ts):
    dt = datetime.fromisoformat(ts)
    is_weekend = dt.weekday() >= 5  # 5 y 6 son sábado y domingo
    if not is_weekend and dt.hour in [8, 9, 14, 15, 20]:  # Horas punta entre semana
        return "peak"
    return "weekend" if is_weekend else "normal"

# Función principal para generar el evento de calidad del aire por zona
def generate_event(zone_name, zone):
    city = "Madrid" 
    country = "Spain"
    ts = datetime.utcnow().isoformat()  # Timestamp actual en formato ISO

    # AQI base + ajustes por tráfico e industria
    base_aqi = random.randint(10, 100)
    industry_boost = int(50 * zone["industry_factor"])
    traffic_boost = int(30 * zone["traffic_factor"])
    pollution = {
        "aqius": base_aqi + industry_boost + traffic_boost,
        "mainus": random.choice(["p1", "p2", "p3"]) 
    }

    # Datos de tráfico simulados
    traffic = {
        "vehicles_count": random.randint(1000, 7000),
        "vehicles_passed": random.randint(50, 200),
        "industrial_activity": random.choice(["low", "moderate", "high"]),
        "environmental_factors": {
            "fire_active": random.choice([True, False]),
            "fire_intensity": random.choice(["low", "medium", "high"])
        }
    }

    # Condiciones específicas de la zona
    zone_conditions = {
        "zone": zone_name,
        "latitude": zone["latitude"],
        "longitude": zone["longitude"],
        "traffic_factor": zone["traffic_factor"],
        "fire_probability": zone["fire_probability"],
        "industry_factor": zone["industry_factor"],
        "vehicles_count": int(random.randint(1000, 7000) * zone["traffic_factor"]),
        "fire_active": random.random() < zone["fire_probability"],
        "industrial_activity": (
            "high" if zone["industry_factor"] > 1
            else "moderate" if zone["industry_factor"] == 1
            else "low"
        )
    }

    # Determinar condición de tráfico (peak, normal, weekend)
    traffic_condition = get_traffic_condition(ts)

    # Calcular AQI ajustado según la situación del momento
    aqi = pollution["aqius"]

    if traffic_condition == "peak":
        aqi += int(zone_conditions["vehicles_count"] * 0.01)  # Aumento por volumen de coches
        aqi += random.randint(5, 15)  # Variación aleatoria extra

    if traffic_condition == "weekend" and zone_conditions["fire_active"]:
        aqi += 100 if traffic["environmental_factors"]["fire_intensity"] == "high" else 50

    if zone_conditions["fire_active"]:
        aqi += 50 if traffic["environmental_factors"]["fire_intensity"] == "low" else 100

    # Estructura del evento final
    event = {
        "city": city,
        "country": country,
        "ts": ts,
        "pollution": pollution,
        "traffic": traffic,
        "location": {
            "latitude": zone["latitude"],
            "longitude": zone["longitude"]
        },
        "zone_conditions": zone_conditions,
        "traffic_condition": traffic_condition,
        "updated_aqi": aqi,
    }

    return event

# Función principal que produce los eventos a Kafka en bucle
def main():
    while True:
        # Crear una lista para los eventos de las 4 zonas
        all_events = []
        
        for zone_name, zone in ZONES.items():
            event = generate_event(zone_name, zone)
            all_events.append(event)  # Guardamos el evento de cada zona
        
        # Enviar todos los eventos de una vez al topic de Kafka
        for event in all_events:
            producer.send("air_quality_topic", value=event)  # Enviar cada evento individualmente
            print(f"Sent to Kafka: {event}")

        producer.flush()  # Asegurar que se envían todos los mensajes
        time.sleep(1)  # Esperar 1 segundo antes de repetir

# Ejecutar main si es el script principal
if __name__ == "__main__":
    main()


