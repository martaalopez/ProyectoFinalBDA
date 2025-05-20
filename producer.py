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

ZONE_STATE = {}

ZONES = {
    "residential": {"latitude": 40.4168, "longitude": -3.7038, "traffic_factor": 0.5, "fire_probability": 0.1, "industry_factor": 0.2, "vehicle_rate": 0.02},
    "industrial":  {"latitude": 40.4168, "longitude": -3.7178, "traffic_factor": 1.5, "fire_probability": 0.05, "industry_factor": 2.0, "vehicle_rate": 0.1},
    "center":      {"latitude": 40.4198, "longitude": -3.7028, "traffic_factor": 2.0, "fire_probability": 0.15, "industry_factor": 1.0, "vehicle_rate": 0.2},
    "suburb":      {"latitude": 40.4567, "longitude": -3.7314, "traffic_factor": 0.3, "fire_probability": 0.25, "industry_factor": 0.5, "vehicle_rate": 0.01},
}

for zone in ZONES:
    ZONE_STATE[zone] = {
        "aqi": random.randint(50, 80),
        "fire_active": False,
        "fire_end_time": None,
        "fire_intensity": None,
        "vehicles_count": 0
    }

SPECIAL_EVENTS = {
    (2024, 1, 1, 18): "concert",
    (2024, 1, 1, 21): "football_match"
}

SIM_TIME = datetime(2024, 1, 1, 12, 0, 0)
SIM_STEP = timedelta(minutes=1)
REAL_SLEEP_TIME = 3

def check_special_event(sim_time):
    return SPECIAL_EVENTS.get((sim_time.year, sim_time.month, sim_time.day, sim_time.hour))

def get_traffic_condition(sim_dt):
    is_weekend = sim_dt.weekday() >= 5
    return "peak" if sim_dt.hour in [8, 9, 14, 15, 20] and not is_weekend else ("weekend" if is_weekend else "normal")

def generate_event(zone_name, zone, sim_time):
    ts = sim_time.isoformat()
    state = ZONE_STATE[zone_name]
    vehicles_passed = int(zone["vehicle_rate"])
    state["vehicles_count"] += vehicles_passed

    fire_duration = random.randint(5, 10) if zone_name == "suburb" else random.randint(3, 6)
    if not state["fire_active"] and random.random() < zone["fire_probability"]:
        state["fire_active"] = True
        state["fire_end_time"] = sim_time + timedelta(minutes=fire_duration)
        state["fire_intensity"] = random.choice(["low", "medium", "high"])
    elif state["fire_active"] and sim_time >= state["fire_end_time"]:
        state["fire_active"] = False
        state["fire_end_time"] = None
        state["fire_intensity"] = None

    special_event = check_special_event(sim_time)
    if special_event:
        vehicles_extra = random.randint(30, 100)
        state["vehicles_count"] += vehicles_extra

    aqi_change = random.randint(-4, 4)
    if state["fire_active"]:
        aqi_change += {"low": 5, "medium": 10, "high": 20}[state["fire_intensity"]]
    else:
        aqi_change -= 2

    aqi_change += int(state["vehicles_count"] * 0.01)

    if zone_name == "industrial":
        aqi_change += int(50 * zone["industry_factor"])

    if special_event:
        aqi_change += 10

    accident_chance = 0.01 if zone_name == "center" else 0.005
    accident_occurred = random.random() < accident_chance
    if accident_occurred:
        aqi_change += 15

    state["aqi"] = max(10, min(500, state["aqi"] + aqi_change))

    # EVENTO PLANO (sin anidaciones)
    event = {
        "city": "Madrid",
        "country": "Spain",
        "ts": ts,
        "pollution_aqius": state["aqi"],
        "pollution_mainus": random.choice(["p1", "p2", "p3"]),
        "vehicles_count": state["vehicles_count"],
        "vehicles_passed": vehicles_passed,
        "industrial_activity": (
            "high" if zone["industry_factor"] > 1
            else "moderate" if zone["industry_factor"] == 1
            else "low"
        ),
        "fire_active": state["fire_active"],
        "fire_intensity": state["fire_intensity"] if state["fire_active"] else "none",
        "accident": "yes" if accident_occurred else "no",
        "latitude": zone["latitude"],
        "longitude": zone["longitude"],
        "zone": zone_name,
        "traffic_factor": zone["traffic_factor"],
        "fire_probability": zone["fire_probability"],
        "industry_factor": zone["industry_factor"],
        "traffic_condition": get_traffic_condition(sim_time),
        "special_event": special_event if special_event else "none",
        "updated_aqi": state["aqi"]
    }

    return event

def main():
    global SIM_TIME
    while True:
        if SIM_TIME.hour >= 12:
            for zone_name, zone in ZONES.items():
                event = generate_event(zone_name, zone, SIM_TIME)
                producer.send("air_quality", value=event)
                print(event)

            producer.flush()

        SIM_TIME += SIM_STEP
        time.sleep(REAL_SLEEP_TIME)

if __name__ == "__main__":
    main()



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

ZONES = {
    "residential": {"latitude": 40.4168, "longitude": -3.7038, "traffic_factor": 0.5, "fire_probability": 0.1, "industry_factor": 0.2, "vehicle_rate": 0.02},
    "industrial":  {"latitude": 40.4168, "longitude": -3.7178, "traffic_factor": 1.5, "fire_probability": 0.05, "industry_factor": 2.0, "vehicle_rate": 0.1},
    "center":      {"latitude": 40.4198, "longitude": -3.7028, "traffic_factor": 2.0, "fire_probability": 0.15, "industry_factor": 1.0, "vehicle_rate": 0.2},
    "suburb":      {"latitude": 40.4567, "longitude": -3.7314, "traffic_factor": 0.3, "fire_probability": 0.25, "industry_factor": 0.5, "vehicle_rate": 0.01},
}

for zone in ZONES:
    ZONE_STATE[zone] = {
        "aqi": random.randint(50, 80),
        "fire_active": False,
        "fire_end_time": None,
        "fire_intensity": None,
        "vehicles_count": 0
    }

# Eventos especiales programados (hora exacta)
SPECIAL_EVENTS = {
    (2024, 1, 1, 18): "concert",
    (2024, 1, 1, 21): "football_match"
}

# Tiempo de simulación
SIM_TIME = datetime(2024, 1, 1, 12, 0, 0)
SIM_STEP = timedelta(minutes=1)           # Cada iteración = 1 minuto simulado
REAL_SLEEP_TIME = 3                       # Cada iteración = 3 segundos reales

def check_special_event(sim_time):
    return SPECIAL_EVENTS.get((sim_time.year, sim_time.month, sim_time.day, sim_time.hour))

def get_traffic_condition(sim_dt):
    is_weekend = sim_dt.weekday() >= 5
    return "peak" if sim_dt.hour in [8, 9, 14, 15, 20] and not is_weekend else ("weekend" if is_weekend else "normal")

def generate_event(zone_name, zone, sim_time):
    ts = sim_time.isoformat()
    state = ZONE_STATE[zone_name]
    vehicles_passed = int(zone["vehicle_rate"])  # simplificado
    state["vehicles_count"] += vehicles_passed

    fire_duration = random.randint(5, 10) if zone_name == "suburb" else random.randint(3, 6)
    if not state["fire_active"] and random.random() < zone["fire_probability"]:
        state["fire_active"] = True
        state["fire_end_time"] = sim_time + timedelta(minutes=fire_duration)
        state["fire_intensity"] = random.choice(["low", "medium", "high"])
    elif state["fire_active"] and sim_time >= state["fire_end_time"]:
        state["fire_active"] = False
        state["fire_end_time"] = None
        state["fire_intensity"] = None

    # EVENTO ESPECIAL
    special_event = check_special_event(sim_time)
    if special_event:
        vehicles_extra = random.randint(30, 100)
        state["vehicles_count"] += vehicles_extra

    aqi_change = random.randint(-4, 4)

    if state["fire_active"]:
        aqi_change += {"low": 5, "medium": 10, "high": 20}[state["fire_intensity"]]
    else:
        aqi_change -= 2

    aqi_change += int(state["vehicles_count"] * 0.01)

    if zone_name == "industrial":
        aqi_change += int(50 * zone["industry_factor"])

    if special_event:
        aqi_change += 10  # eventos especiales generan más contaminación

    # PROBABILIDAD DE ACCIDENTE
    accident_chance = 0.01 if zone_name == "center" else 0.005
    accident_occurred = random.random() < accident_chance
    if accident_occurred:
        aqi_change += 15

    state["aqi"] = max(10, min(500, state["aqi"] + aqi_change))
    pollution = {
        "aqius": state["aqi"],
        "mainus": random.choice(["p1", "p2", "p3"])
    }

    event = {
        "city": "Madrid",
        "country": "Spain",
        "ts": ts,
        "pollution": pollution,
        "traffic": {
            "vehicles_count": state["vehicles_count"],
            "vehicles_passed": vehicles_passed,
            "industrial_activity": (
                "high" if zone["industry_factor"] > 1
                else "moderate" if zone["industry_factor"] == 1
                else "low"
            ),
            "environmental_factors": {
                "fire_active": state["fire_active"],
                "fire_intensity": state["fire_intensity"] if state["fire_active"] else "none"
            },
            "accident": "yes" if accident_occurred else "no"
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
            "fire_active": state["fire_active"]
        },
        "traffic_condition": get_traffic_condition(sim_time),
        "special_event": special_event if special_event else "none",
        "updated_aqi": state["aqi"]
    }

    return event

def main():
    global SIM_TIME
    while True:
        if SIM_TIME.hour >= 12:
            all_events = []
            for zone_name, zone in ZONES.items():
                event = generate_event(zone_name, zone, SIM_TIME)
                all_events.append(event)

            for event in all_events:
                producer.send("air_quality_topic", value=event)
                producer.send("air_quality", value=event)
                print(event)

            producer.flush()

        SIM_TIME += SIM_STEP  # avanzar 1 minuto simulado
        time.sleep(REAL_SLEEP_TIME)  # esperar 3 segundos reales

if __name__ == "__main__":
    main()
