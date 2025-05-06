from kafka import KafkaProducer
from datetime import datetime, timedelta
import random
import json
import time

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='192.168.11.10:9094',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Estado persistente de cada zona
ZONE_STATE = {}

# Definir zonas con tasas de paso de vehículos por segundo
ZONES = {
    "residential": {"latitude": 40.4168, "longitude": -3.7038, "traffic_factor": 0.5, "fire_probability": 0.1, "industry_factor": 0.2, "vehicle_rate": 0.02},  # 0.02 vehículos por segundo
    "industrial":  {"latitude": 40.4168, "longitude": -3.7178, "traffic_factor": 1.5, "fire_probability": 0.05, "industry_factor": 2.0, "vehicle_rate": 0.1},  # 0.1 vehículos por segundo
    "center":      {"latitude": 40.4198, "longitude": -3.7028, "traffic_factor": 2.0, "fire_probability": 0.15, "industry_factor": 1.0, "vehicle_rate": 0.2},  # 0.2 vehículos por segundo
    "suburb":      {"latitude": 40.4567, "longitude": -3.7314, "traffic_factor": 0.3, "fire_probability": 0.25, "industry_factor": 0.5, "vehicle_rate": 0.01},  # 0.01 vehículos por segundo
}

# Inicializar estado de cada zona
for zone in ZONES:
    ZONE_STATE[zone] = {
        "aqi": random.randint(50, 80),
        "fire_active": False,
        "fire_end_time": None,
        "fire_intensity": None,
        "vehicles_count": 0  # Inicializar el contador de vehículos
    }

def get_traffic_condition(ts):
    dt = datetime.fromisoformat(ts)
    is_weekend = dt.weekday() >= 5
    return "peak" if dt.hour in [8, 9, 14, 15, 20] and not is_weekend else ("weekend" if is_weekend else "normal")

def generate_event(zone_name, zone):
    now = datetime.utcnow()
    ts = now.isoformat()
    state = ZONE_STATE[zone_name]

    # Simular el paso de vehículos durante un segundo
    vehicles_passed_in_second = int(zone["vehicle_rate"])  # Número de vehículos que pasan en un segundo
    state["vehicles_count"] += vehicles_passed_in_second

    # Modificar probabilidad y duración del fuego según la zona
    if zone_name == "suburb":
        fire_duration = random.randint(5, 10)  # Fuego más largo en suburb
    else:
        fire_duration = random.randint(3, 6)  # Duración normal en otras zonas
    
    # Simular fuego por tiempo
    if not state["fire_active"] and random.random() < zone["fire_probability"]:
        state["fire_active"] = True
        state["fire_end_time"] = now + timedelta(minutes=fire_duration)
        state["fire_intensity"] = random.choice(["low", "medium", "high"])
    elif state["fire_active"] and now >= state["fire_end_time"]:
        state["fire_active"] = False
        state["fire_end_time"] = None
        state["fire_intensity"] = None

    # Ajustar la calidad del aire según la cantidad de vehículos
    aqi_change = random.randint(-4, 4)
    if state["fire_active"]:
        if state["fire_intensity"] == "low":
            aqi_change += 5
        elif state["fire_intensity"] == "medium":
            aqi_change += 10
        else:
            aqi_change += 20
    else:
        aqi_change -= 2  # mejora si no hay fuego

    # Calcular el impacto del tráfico en la calidad del aire
    aqi_change += int(state["vehicles_count"] * 0.01)  # El número de vehículos afecta la calidad del aire
    
    # Considerar el factor industrial en zonas industriales
    if zone_name == "industrial":
        aqi_change += int(50 * zone["industry_factor"])  # Mayor factor industrial, peor calidad del aire
    
    # Calcular el AQI final para la zona
    state["aqi"] = max(10, min(500, state["aqi"] + aqi_change))
    pollution = {
        "aqius": state["aqi"],
        "mainus": random.choice(["p1", "p2", "p3"])
    }

    traffic_condition = get_traffic_condition(ts)

    event = {
        "city": "Madrid",
        "country": "Spain",
        "ts": ts,
        "pollution": pollution,
        "traffic": {
            "vehicles_count": state["vehicles_count"],
            "vehicles_passed": vehicles_passed_in_second,
            "industrial_activity": (
                "high" if zone["industry_factor"] > 1
                else "moderate" if zone["industry_factor"] == 1
                else "low"
            ),
            "environmental_factors": {
                "fire_active": state["fire_active"],
                "fire_intensity": state["fire_intensity"] if state["fire_active"] else "none"
            }
        },
        "location": {
            "latitude": zone["latitude"],
            "longitude": zone["longitude"]
        },
        "zone_conditions": {
            "zone": zone_name,
            "latitude": zone["latitude"],
            "longitude": zone["longitude"],
            "traffic_factor": zone["traffic_factor"],
            "fire_probability": zone["fire_probability"],
            "industry_factor": zone["industry_factor"],
            "vehicles_count": state["vehicles_count"],
            "fire_active": state["fire_active"],
            "industrial_activity": (
                "high" if zone["industry_factor"] > 1
                else "moderate" if zone["industry_factor"] == 1
                else "low"
            )
        },
        "traffic_condition": traffic_condition,
        "updated_aqi": state["aqi"]
    }

    return event

def main():
    while True:
        all_events = []
        for zone_name, zone in ZONES.items():
            event = generate_event(zone_name, zone)
            all_events.append(event)
        
        for event in all_events:
            producer.send("air_quality_topic", value=event)
            print(event)
        
        producer.flush()
        time.sleep(1)

if __name__ == "__main__":
    main()
