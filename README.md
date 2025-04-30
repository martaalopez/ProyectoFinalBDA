# Proyecto Final BDA 2024-25

![ChatGPT Image 26 abr 2025, 12_03_57](https://github.com/user-attachments/assets/6102e595-1fdc-4c95-bc74-89ab9ad7bd9c)

## 1.Introducción

Hoy en dia la calidad del aire y la contaminacion son factores ambientales muy preocupantes en nuestra sociedad .El trafico  diario de vehiculos ,tanto de personas que van al trabajo como de padres q van a llevar a sus hijos al colegio son factores que hacen que aumente  el deterioro de la calidad de aire.
Además algunos fenómenos naturales como los incendios forestales pueden tener un fuerte impacto en la contaminación atmosférica,al igual que la actividad industrial,donde las emisiones de humo y partículas contaminantes se mezclan con la atmósfera, empeorando aún más la situación.

Esto puede hacer que existan consecuencias directas en la salud publica, un articulo  revela que 2000 niños mueren cada dia en el mundo por mal calidad del aire,por ello he decidido hacer una investigación que se enfoca en el monitoreo y análisis de los principales factores que afectan la calidad del aire, con el objetivo de identificar los eventos más frecuentes y críticos. A partir de estos datos, espero poder extraer conclusiones que contribuyan a diseñar soluciones eficientes para combatir este grave problema global.
  

## 2.Fuente de Informacion

Para poder abarcar con todo esto vamos a apoyarnos en los datos proporcionados  por la AirVisual API la cual  ofrece información sobre el tiempo, la calidad del aire y los incendios activos,etc...
Sin embargo, esta API presenta un problema:los datos se actualizan cada hora , mientras que nuestro objetivo es realizar un monitoreo en tiempo real, actualizando los datos cada minuto.

Por ello vamos a generar  unos datos sinteticos,  incluyendo no solo las variables básicas ofrecidas por la API, sino también otros datos adicionales que considero relevantes para un análisis más completo:
En terminos generales tendriamos estos datos
-Casos de enfermedades respiratorias detectadas por minuto.
-Número de vehículos circulando en la vía pública.
-Información sobre incendios activos.
-Nivel de actividad industrial.
-Calidad del aire (AQI) y contaminante principal (mainus).
-Lugar

### 2.1 Estructura de datos 
En este apartado vamos a especificar la estructura de nuestro datos

### Ejemplo de datos:
````

{
  "city": "Eilat",
  "country": "Israel",
  "ts": "2017-02-01T01:15:00.000Z",
  "pollution": {
    "aqius": 18,
    "mainus": "p1" 
  },
  "health": {
    "asthma_cases": 2,
    "bronchitis_cases": 1,
    "copd_cases": 0,
    "total_respiratory_cases": 3
  },
  "traffic": {
    "vehicles_count": 1000,
    "industrial_activity": "moderate",
    "environmental_factors": {
      "fire_active": true,
      "fire_intensity": "high"
    }
  }
}


````

## 2.2 Explicación de los Campos

A continuación se describen los campos que componen la estructura de datos:

- **`city`**:  
  Nombre de la ciudad donde se realiza la medición.  
  Ejemplo: `"Eilat"`.

- **`country`**:  
  País al que pertenece la ciudad donde se recogen los datos.  
  Ejemplo: `"Israel"`.

- **`ts`**:  
  Timestamp o fecha y hora exacta en que se tomó la medición, en formato ISO 8601.  
  Ejemplo: `"2017-02-01T01:15:00.000Z"`.

- **`pollution.aqius`**:  
  Índice de calidad del aire basado en el estándar de Estados Unidos (US AQI).  
  Un valor bajo indica buena calidad del aire, mientras que uno alto indica mala calidad.  
  Ejemplo: `18`.

- **`pollution.mainus`**:  
  Principal contaminante detectado en el aire según el estándar de EE.UU.  
  Ejemplo: `"p1"` (donde "p1" normalmente representa partículas PM2.5).

- **`health.asthma_cases`**:  
  Número de casos de asma detectados.  
  Ejemplo: `2`.

- **`health.bronchitis_cases`**:  
  Número de casos de bronquitis detectados.  
  Ejemplo: `1`.

- **`health.copd_cases`**:  
  Número de casos de EPOC (Enfermedad Pulmonar Obstructiva Crónica) registrados.  
  Ejemplo: `0`.

- **`health.total_respiratory_cases`**:  
  Total de enfermedades respiratorias registradas (asma + bronquitis + EPOC).  
  Ejemplo: `3`.

- **`traffic.vehicles_count`**:  
  Número de vehículos en circulación detectados en el área de monitoreo.  
  Ejemplo: `1000`.

- **`traffic.industrial_activity`**:  
  Nivel de actividad industrial en la zona. Puede tomar valores como `"low"`, `"moderate"`, o `"high"`.  
  Ejemplo: `"moderate"`.

- **`traffic.environmental_factors.fire_active`**:  
  Indicador booleano que muestra si hay un incendio activo (`true`) o no (`false`).  
  Ejemplo: `true`.

- **`traffic.environmental_factors.fire_intensity`**:  
  Nivel de intensidad del incendio detectado. Puede ser `"low"`, `"moderate"` o `"high"`.  
  Ejemplo: `"high"`.
  
## 3. Requisitos
Debe haber como mínimo 3 nodos en los clusters (en cada uno):
Hadoop (HDFS/Yarn)
![image](https://github.com/user-attachments/assets/bbe8c104-5059-4658-88ab-952a1f15c1cb)
![image](https://github.com/user-attachments/assets/ee90e9d2-2931-43d7-b1bb-297e8eb30cb9)

Spark
![image](https://github.com/user-attachments/assets/4a360f4a-3007-4646-92e2-289e0c5d676c)

Kafka
![image](https://github.com/user-attachments/assets/1803b1be-1aea-4d21-8c91-63ead014e844)


````
  import json
import time
import random
from datetime import datetime, timedelta
from faker import Faker
from kafka import KafkaProducer

# Inicializar Faker
fake = Faker()

# Configuración de Kafka
producer = KafkaProducer(
    bootstrap_servers='192.168.11.10:9094',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Ciudades grandes y ciudades con naturaleza
large_cities = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza"]
nature_cities = ["Granada", "Palma", "Santander", "Oviedo", "Vitoria"]

# Lista completa de ciudades en España
cities = large_cities + nature_cities + ["Málaga", "Murcia"]

# Variables de simulación
entradas_escalonadas = True
usar_bicis = True

# Inicialización de los casos acumulados
acumulados = {
    "asthma_cases": 0,
    "bronchitis_cases": 0,
    "copd_cases": 0,
    "total_respiratory_cases": 0
}

def generate_data():
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()  # 0 lunes - 6 domingo

    # Selección de ciudad
    city = random.choice(cities)
    country = "España"

    # Tráfico base
    vehicles_count = random.randint(500, 1500)

    # Aumentar tráfico según la hora
    if hour in [8, 14, 20]:
        vehicles_count = random.randint(4000, 7000)

    # Si es fin de semana, reducir tráfico
    if weekday >= 5:
        vehicles_count = int(vehicles_count * 0.5)

    # Simulación de entradas escalonadas
    if entradas_escalonadas and hour == 8:
        vehicles_count = int(vehicles_count * 0.6)

    # Simulación de bicicletas
    if usar_bicis:
        vehicles_count = int(vehicles_count * 0.7)

    # Nivel de actividad industrial
    industrial_activity = random.choice(["low", "moderate", "high"])

    # AQI inicial
    aqi = random.randint(10, 50)

    # Más contaminación en ciudades grandes
    if city in large_cities:
        aqi += random.randint(50, 100)

    # Incendios
    fire_active = False
    fire_intensity = None

    prob_fire = 0.7 if city in nature_cities else 0.2
    if random.random() < prob_fire:
        fire_active = True
        fire_intensity = random.choice(["low", "moderate", "high"])

        # Si hay incendio, subir AQI
        aqi += random.randint(30, 70)
        if fire_intensity == "high":
            aqi += 100

    # Simulación de enfermedades respiratorias
    base_health_cases = random.randint(0, 2)
    if city in large_cities:
        base_health_cases += random.randint(1, 5)

    # Casos acumulados
    global acumulados
    new_asthma_cases = random.randint(0, base_health_cases)
    new_bronchitis_cases = random.randint(0, base_health_cases - new_asthma_cases)
    new_copd_cases = base_health_cases - new_asthma_cases - new_bronchitis_cases

    acumulados["asthma_cases"] += new_asthma_cases
    acumulados["bronchitis_cases"] += new_bronchitis_cases
    acumulados["copd_cases"] += new_copd_cases
    acumulados["total_respiratory_cases"] = (
        acumulados["asthma_cases"] +
        acumulados["bronchitis_cases"] +
        acumulados["copd_cases"]
    )

    data = {
        "city": city,
        "country": country,
        "ts": now.isoformat(),
        "pollution": {
            "aqius": aqi,
            "mainus": random.choice(["p1", "p2", "o3", "co", "so2", "no2"])
        },
        "health": {
            "asthma_cases": acumulados["asthma_cases"],
            "bronchitis_cases": acumulados["bronchitis_cases"],
            "copd_cases": acumulados["copd_cases"],
            "total_respiratory_cases": acumulados["total_respiratory_cases"]
        },
        "traffic": {
            "vehicles_count": vehicles_count,
            "industrial_activity": industrial_activity,
            "environmental_factors": {
                "fire_active": fire_active,
                "fire_intensity": fire_intensity if fire_active else "none"
            }
        }
    }

    return data

def main():
    print("Simulación de datos en tiempo real (minuto a minuto)... Ctrl+C para detener.")
    try:
        while True:
            start_time = time.time()

            generated_data = generate_data()

            # Enviar a Kafka
            producer.send('air_quality', value=generated_data)
            print(f"Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {generated_data}")

            producer.flush()

            # Esperar hasta completar 60 segundos exactos
            elapsed_time = time.time() - start_time
            sleep_time = max(60.0 - elapsed_time, 0)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nSimulación detenida.")

if __name__ == "__main__":
    main()
````





