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



## 4.Actualización de la nueva versión de kafka

La versión que tenemos actualmente es la 3.9.0 tenemos que actulizarla a la 4.0.0 
![image](https://github.com/user-attachments/assets/452c991f-933a-424f-834b-cc165a3d906f)
![image](https://github.com/user-attachments/assets/edd70d7f-7d7f-4f51-a9da-361b080c9e23)
![image](https://github.com/user-attachments/assets/ab9e9c8f-4181-4f47-a0b4-9b6b899b439b)
![image](https://github.com/user-attachments/assets/af891f4c-b579-411c-ac09-16af7a717ca2)

Apache Kafka puede ser iniciado usando KRaft

Kafka con KRaft
Kafka se puede ejecutar usando el modo KRaft mediante scripts locales y archivos descargados o mediante la imagen de docker

Usando los archivos descargados

Genera un cluster UUID

KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
Formatea el directorio de log

bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties 
Ejecuta el servidor Kafka

bin/kafka-server-start.sh config/server.properties


## 5.Configuración del Clúster de Kafka 
1.Vamos a establecer todos los archivos de configuración en una carpeta de ejemplo llamada proyectoBDA_MLU, que en mi caso estará alojada en /opt/kafka/proyecto_MLU
![image](https://github.com/user-attachments/assets/e12ef486-f0bd-4ca7-b4fa-3a83788f20b7)

Dado que todas las instancias se ejecutarán en el mismo nodo, es crucial asignar puertos únicos y directorios de log para cada broker y el controller.

Configuración:
Para el controller, debemos usar como base la configuración de propiedades de controller de kafka (KRaft mode) que se encuentran config/kraft/controller.properties
Para cada broker, necesitaremos crear un archivo de configuración por separado. Para ello debemos usar como base la configuración de propiedades de brokers de kafka que se encuentran config/kraft/broker.properties

Creamos los directorios necesarios para nuestro proyecto_MLU

````
mkdir -p /opt/kafka/proyecto_MLU/config
mkdir -p /opt/kafka/proyecto_MLU/logs
````
Hacemos 2 y 1 copia de los ficheros correspondientes de configuración para cada uno

````

cp /opt/kafka_2.13-4.0.0/config/controller.properties /opt/kafka/proyecto_MLU/config/controller1.properties
cp /opt/kafka_2.13-4.0.0/config/broker.properties /opt/kafka/proyecto_MLU/config/broker1.properties
cp /opt/kafka_2.13-4.0.0/config/broker.properties /opt/kafka/proyecto_MLU/config/broker2.properties

````
![image](https://github.com/user-attachments/assets/a09f55ca-0843-4a9b-bb60-9bb8f572f8e8)

Asignamos la configuración al controller

````
# Server Basics
process.roles=controller
node.id=1
controller.quorum.bootstrap.servers=192.168.11.10:9093
# Socket Server Settings
listeners=CONTROLLER://localhost:9093
controller.listener.names=CONTROLLER
# Log Basics
log.dirs=/opt/kafka/proyecto_MLU/logs/controller1
````
Asignamos la siguiente configuración para cada broker

````
# Server Basics
process.roles=broker
node.id=2
controller.quorum.bootstrap.servers=192.168.11.10:9093
# Socket Server Settings
listeners=PLAINTEXT://192.168.11.10:9094
inter.broker.listener.name=PLAINTEXT
advertised.listeners=PLAINTEXT://192.168.11.10:9094
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
# Log Basics
log.dirs=/opt/kafka/proyecto_MLU/logs/broker1
````
````
# Server Basics
process.roles=broker
node.id=3
controller.quorum.bootstrap.servers=192.168.11.10:9093
# Socket Server Settings
listeners=PLAINTEXT://192.168.11.10:9095
inter.broker.listener.name=PLAINTEXT
advertised.listeners=PLAINTEXT://192.168.11.10:9095
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
# Log Basics
log.dirs=/opt/kafka/proyecto_MLU/logs/broker2
````
Creamos los workers
````
   nano /opt/kafka/proyecto_MLU/config/worker1.properties
````
````
bootstrap.servers=localhost:9094,localhost:9095
group.id=connect-cluster
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=true
value.converter.schemas.enable=true
offset.storage.topic=connect-offsets
offset.storage.replication.factor=2
config.storage.topic=connect-configs
config.storage.replication.factor=2
status.storage.topic=connect-status
status.storage.replication.factor=2
plugin.path=/opt/kafka/proyecto_MLU/libs
listeners=http://localhost:8083
````
````
 nano /opt/kafka/proyecto_MLU/config/worker2.properties
`````
````
bootstrap.servers=localhost:9094,localhost:9095
group.id=connect-cluster
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=true
value.converter.schemas.enable=true
offset.storage.topic=connect-offsets
offset.storage.replication.factor=2
config.storage.topic=connect-configs
config.storage.replication.factor=2
status.storage.topic=connect-status
status.storage.replication.factor=2
plugin.path=/opt/kafka/proyecto_MLU/libs
listeners=http://localhost:8084

````
Iniciamos Kafka
````
KAFKA_CLUSTER_ID="$(/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh random-uuid)"
echo $KAFKA_CLUSTER_ID
````
![image](https://github.com/user-attachments/assets/eb9b2605-8862-43f8-bb7d-7f7c47474a31)

#Formateamos los directorios de log
````
/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID --standalone -c /opt/kafka/proyecto_MLU/config/controller1.properties
/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c /opt/kafka/proyecto_MLU/config/broker1.properties
/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c /opt/kafka/proyecto_MLU/config/broker2.properties
````
![image](https://github.com/user-attachments/assets/1ab03493-51c0-4fff-aeae-ff9e5e469d62)

Iniciamos los server(1 controller y 2 brokers) cada uno en una terminal

````
#Ejecuta el servidor Kafka
/opt/kafka_2.13-4.0.0/bin/kafka-server-start.sh /opt/kafka/proyecto_MLU/config/controller1.properties
/opt/kafka_2.13-4.0.0/bin/kafka-server-start.sh /opt/kafka/proyecto_MLU/config/broker1.properties
/opt/kafka_2.13-4.0.0/bin/kafka-server-start.sh /opt/kafka/proyecto_MLU/config/broker2.properties
````

 Creación del Topic
Creamos el topic con factor de replica 2 y 3 particiones. El topic debe conectarse a un broker.
````
/opt/kafka_2.13-4.0.0/bin/kafka-topics.sh --create --topic air-quality --bootstrap-server 192.168.11.10:9094 --replication-factor 2 --partitions 4
````
![image](https://github.com/user-attachments/assets/1ae0aafe-e850-437c-a781-9aa21d2dc3ba)

Creamos el producer.py

![image](https://github.com/user-attachments/assets/32c45acc-f051-4c7e-88e7-e2d7afb407b1)

````
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 --master spark://192.168.11.10:7077 /opt/kafka/proyecto_MLU/consumer.py
````
















