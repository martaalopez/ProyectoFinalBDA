# Proyecto Final BDA 2024-25

 <!-- ![ChatGPT Image 26 abr 2025, 12_03_57](https://github.com/user-attachments/assets/6102e595-1fdc-4c95-bc74-89ab9ad7bd9c)

-->

## Índice

1. [Introducción](#1-introducción)
2. [Fuente de Información](#2-fuente-de-información)
3. [Requisitos](#3-requisitos)
4. [Configuración del Clúster de Kafka](#4-configuración-del-clúster-de-kafka)
5. [Levantamos Sistemas](#5-levantamos-sistemas)
   - [5.1 Levantamos HDFS](#51-levantamos-hdfs-hadoop-distributed-file-system)
   - [5.2 Arrancamos Spark Master y Workers](#52-arrancamos-spark-master-y-workers)
   - [5.3 Iniciamos Kafka](#53-iniciamos-kafka-controller--brokers)
   - [5.4 Creamos el Topic Kafka](#54-creamos-el-topic-kafka)
   - [5.5 Creación de la tabla en MySQL](#55-creación-de-la-tabla-en-mysql)
   - [5.6 Creación del producer y del consumer](#56-creación-del-producer-y-del-consumer)
     - [5.6.1 Ejecutamos el Consumer](#561-ejecutamos-el-consumer)
     - [5.6.2 Ejecutamos el Producer Kafka](#562-ejecutamos-el-producer-kafka)
     - [5.6.3 Visualizamos la información](#563-visualizamos-la-información)
6. [Visualización en PowerBI](#6-visualización-en-powerbi)
   - [6.1 Promedio de AQI](#61-promedio-de-aqi)
   - [6.2 Análisis de Calidad del Aire (AQI) en Zonas Industriales](#62-análisis-de-calidad-del-aire-aqi-en-zonas-industriales)
   - [6.3 Análisis del Impacto de Incendios en la Calidad del Aire](#63-análisis-del-impacto-de-incendios-en-la-calidad-del-aire-aqi-en-zona-suburbana)
   - [6.4 Promedio de Vehículos por Minuto y AQI por Zona](#64-promedio-de-vehículos-por-minuto-y-aqi-por-zona)
   - [6.5 Distribución del AQI por Día de la Semana](#65-distribución-del-aqi-por-día-de-la-semana)
7. [Prometheus](#7-prometheus)
8. [Grafana](#8-grafana)


## 1. Introducción

Hoy en día, la calidad del aire y la contaminación son factores ambientales que generan gran preocupación en nuestra sociedad.
El tráfico diario de vehículos es una de las principales causas del deterioro de la calidad del aire.
Además,ciertos fenómenos naturales como los incendios forestales pueden tener un impacto significativo en la contaminación atmosférica.A esto se le suma la actividad industrial,cuyas emisiones de humo y partículas contaminantes se mezclan con la atmósfera, agravando aún más la situación.

Esto puede hacer que existan consecuencias directas en la salud publica,un artículo  revela que 2000 niños mueren cada dia en el mundo por mal calidad del aire,por ello he decidido hacer una investigación que se enfoca en el monitoreo y análisis de los principales factores que afectan la calidad del aire,con el objetivo de identificar los eventos más frecuentes y críticos.A partir de estos datos,espero poder extraer conclusiones que contribuyan a diseñar soluciones eficientes para combatir este grave problema global.
  

## 2. Fuente de Información

Para poder abarcar con todo esto vamos a apoyarnos en los datos proporcionados por la AirVisual API la cual ofrece información sobre el tiempo, la calidad del aire y los incendios activos,etc...
Sin embargo,esta API presenta un problema:los datos se actualizan cada hora ,mientras que nuestro objetivo es realizar un monitoreo en tiempo real,actualizando los datos cada segundo.

Por ello vamos a generar  unos datos sinteticos,incluyendo no solo las variables básicas ofrecidas por la API,sino también otros datos adicionales que considero relevantes para un análisis más completo,como el tráfico,la actividad industrial y la probabilidad de incendios.
Los datos ficticios se recogerán desde sensores virtuales distribuidos en cuatro zonas distintas de Madrid:
Centro: La cual tiene un alto volumen de tráfico
Residencial: Es un área más residencial con menos tráfico de vehículos.
Industrial: Es una zona con alta actividad industrial,donde predominan los contaminantes derivados del humo y procesos fabriles.
Suburbana: Es una zona de factores naturales y con una mayor probabilidad de incendios forestales.

## 3. Requisitos
Debe haber como mínimo 3 nodos en los clusters (en cada uno):

-Hadoop (HDFS/Yarn)
Hadoop es el sistema responsable del almacenamiento distribuido de grandes volúmenes de datos (HDFS) y de la gestión de recursos y ejecución de tareas distribuidas (YARN).

Contar con al menos tres nodos en el cluster Hadoop permite:

Distribuir los datos entre múltiples máquinas (DataNodes).

Mantener un nodo maestro (NameNode) que coordina la lectura y escritura en el sistema de archivos.

Asegurar la replicación de los datos en diferentes nodos para prevenir pérdidas en caso de fallos.
![image](https://github.com/user-attachments/assets/bbe8c104-5059-4658-88ab-952a1f15c1cb)

![image](https://github.com/user-attachments/assets/ee90e9d2-2931-43d7-b1bb-297e8eb30cb9)


-Spark
Apache Spark es el motor encargado del procesamiento distribuido de los datos.A diferencia de Hadoop MapReduce,Spark permite trabajar en memoria,lo que lo hace mucho más rápido y eficiente para el análisis de grandes volúmenes de datos.

Tener tres nodos como mínimo en el cluster Spark ofrece :

Una distribución paralela del procesamiento.

Coordinar las tareas desde el nodo maestro.

Ejecución simultánea de trabajos en los nodos trabajadores (Workers).

![image](https://github.com/user-attachments/assets/4a360f4a-3007-4646-92e2-289e0c5d676c)


-Kafka
Apache Kafka es la tecnología utilizada para gestionar el flujo de mensajes en tiempo real. En este proyecto,Kafka se encarga de transmitir los eventos generados por los sensores virtuales (como los datos de calidad del aire, tráfico, incendios, etc.).
Se ha actualizado Kafka a la versión 4.0.0,lo que introduce una mejora importante:la eliminación de la dependencia de Zookeeper,gracias al nuevo sistema de metadatos KRaft (Kafka Raft Metadata mode).

![image](https://github.com/user-attachments/assets/1d2feb40-6772-4ea7-9e3f-e7edf1420f69)


## 4. Configuración del Clúster de Kafka
1.Vamos a establecer todos los archivos de configuración en una carpeta llamada proyectoBDA_MLU,que en mi caso estará alojada en /opt/kafka/proyecto_MLU

![image](https://github.com/user-attachments/assets/e12ef486-f0bd-4ca7-b4fa-3a83788f20b7)

Creamos los directorios necesarios para nuestro proyecto_MLU

````
mkdir -p /opt/kafka/proyecto_MLU/config
mkdir -p /opt/kafka/proyecto_MLU/logs
````

En nuestra arquitectura vamos a tener lo siguiente:
Un controller que va a ser el nodo responsable de poder coordinar el clúster.Se va a encargar de gestionar los eventos como la creación y eliminación de topics,la asignaciñon de particiones y la detección de fallos en los brokers.
Para el controller,debemos usar como base la configuración de propiedades de controller de kafka que se encuentran config/controller.properties

Dos brokers,donde cada uno va a estar identificado por un Id y va a contener ciertas particiones de un topic.Va a permitir replicar y poder particionar dichos topics balanceando la carga de almacenamiento entre los brokers.
Para cada broker,necesitaremos crear un archivo de configuración por separado.Para ello debemos usar como base la configuración de propiedades de brokers de kafka que se encuentran config//broker.properties

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

## 5. Levantamos Sistemas
Vamos a activar todos los servicios para que nuestro flujo de datos pueda funcionar de manera correcta.

### 5.1 Levantamos HDFS (Hadoop Distributed File System)
Levantamos HDFS que será nuestro sistema de almacenamiento distribuido,donde los datos procesados se guardarán.
Se inician los servicios del NameNode y los DataNodes,permitiendo el almacenamiento distribuido de grandes volúmenes de datos.
Se activa YARN,que gestionará los recursos y la ejecución de procesos en los distintos nodos del clúster.
Esto asegura que todo lo que se procese o almacene posteriormente tenga soporte escalable y tolerante a fallos.
````
cd $HADOOP_HOME
stop-dfs.sh
start-dfs.sh

# Verificamos que el sistema no este en modo seguro 
hdfs dfsadmin -safemode get
hdfs dfsadmin -safemode leave
````
### 5.2 Arrancamos Spark Master y Workers
Reiniciamos el Spark Master y los Workers del clúster utilizando los scripts provistos por Spark.
Spark será el encargado de leer los datos desde Kafka y analizarlos en tiempo real.
Al reiniciar el Spark Master y varios Spark Workers, aseguramos que el entorno esté limpio y listo para el procesamiento paralelo de grandes volúmenes de datos.
````
/opt/hadoop-3.4.1/spark-3.5.4/sbin/stop-all.sh
/opt/hadoop-3.4.1/spark-3.5.4/sbin/start-all.sh
````

### 5.3 Iniciamos Kafka (Controller + Brokers)
Como más adelante utilizaremos Prometheus y Grafana,se ha preparado un script personalizado llamado kafka-server-start_proyecto_MLU.sh adaptado especialmente para este proyecto.

1.Configurar Prometheus
Tras a ver instalado prometheus,duplicamos el archivo de configuración por defecto y creamos uno específico para el proyecto.
Este script está diseñado para poder iniciar instancias de Kafka personalizadas para el proyecto, específicamente configuradas para que cada broker y controller de Kafka use un puerto diferente , asi evitamos errores de conflictor de red  y monitoreo al ejecutar múltiples nodos Kafka en la misma máquina .
````
cp /opt/prometheus-2.53.4/prometheus.yml /opt/prometheus-2.53.4/prometheus_proyecto_MLU.yml
nano /opt/prometheus-2.53.4/prometheus_proyecto_MLU.yml
````
Dentro del archivo prometheus_proyecto_MLU.yml, usamos la siguiente configuración:
````
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "kafka"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: [
        "localhost:11001", # Controller 1 (node.id=1)
        "localhost:11002", # Broker 1 (node.id=2)
        "localhost:11003", # Broker 3 (node.id=3)
      ]
````

2.Creamos el script de inicio de Kafka personalizado
Creamos y editamos el siguiente archivo:
````
nano /opt/kafka_2.13-4.0.0/bin/kafka-server-start_proyecto_MLU.sh
````
En este script vamos  una configuración adicional para habilitar JMX Exporter,lo que permitirá monitorear los nodos de Kafka con Prometheus.
El siguiente fragmento se añade al inicio del script para activar el agente de monitoreo JMX Exporter según el node.id configurado en cada server.properties:
````
# --- INICIO DE MODIFICACIÓN PARA JMX EXPORTER ---

# Establecemos KAFKA_OPTS por defecto si no está definido
KAFKA_OPTS=${KAFKA_OPTS:-}

# Encontrar la ruta al archivo server.properties (o cualquier archivo .properties)
PROPERTIES_FILE=""
for arg in "$@"; do
  if [[ "$arg" == *".properties" ]]; then
    PROPERTIES_FILE="$arg"
    break
  fi
done

# Variables para JMX Exporter
JMX_AGENT_PATH="/opt/kafka_2.13-4.0.0/libs/jmx_prometheus_javaagent-1.2.0.jar"
# Ruta al archivo de configuración del JMX Exporter. Si no usas uno, déjala vacía pero mantén el ':' en el argumento final.
JMX_CONFIG_FILE="/opt/kafka_2.13-4.0.0/config/jmx-exporter-kafka.yml"

# Lógica para determinar el puerto y configurar KAFKA_OPTS
NODE_ID=""
JMX_PORT=""
JMX_JAVAAGENT_ARG=""

# 1. Intentar extraer node.id del archivo properties
if [ -n "$PROPERTIES_FILE" ] && [ -f "$PROPERTIES_FILE" ]; then
    NODE_ID=$(grep "^[[:space:]]*node.id[[:space:]]*=" "$PROPERTIES_FILE" | head -1 | sed "s/^[[:space:]]*node.id[[:space:]]*=//" | cut -d'#' -f1 | tr -d '[:space:]')
fi

# 2. Validar NODE_ID y calcular JMX_PORT
if ! [[ "$NODE_ID" =~ ^[0-9]+$ ]]; then
    echo "WARNING: JMX Exporter: No se pudo determinar el node.id del archivo $PROPERTIES_FILE o no es un número válido ('$NODE_ID')." >&2
    echo "WARNING: JMX Exporter NO será cargado para esta instancia de Kafka." >&2
# 3. Validar si el JAR del JMX Exporter existe y es legible
elif [ ! -r "$JMX_AGENT_PATH" ]; then
    echo "ERROR: JMX Exporter: El archivo JAR NO se encuentra o no es legible: $JMX_AGENT_PATH" >&2
    echo "WARNING: JMX Exporter NO será cargado para esta instancia de Kafka." >&2
# 4. Validar si el archivo de configuración existe y es legible (si se especificó uno)
elif [ -n "$JMX_CONFIG_FILE" ] && [ ! -r "$JMX_CONFIG_FILE" ]; then
    echo "ERROR: JMX Exporter: El archivo de configuración NO se encuentra o no es legible: $JMX_CONFIG_FILE" >&2
    echo "WARNING: JMX Exporter NO será cargado para esta instancia de Kafka." >&2
# 5. Si todas las validaciones pasan, construir el argumento y configurar KAFKA_OPTS
else
    JMX_BASE_PORT=11000 # Puerto base, JMX_PORT = JMX_BASE_PORT + NODE_ID
    JMX_PORT=$((JMX_BASE_PORT + NODE_ID))

    # Construir el argumento del javaagent: =puerto:/ruta/config (o =puerto:)
    JMX_JAVAAGENT_ARG="-javaagent:$JMX_AGENT_PATH=$JMX_PORT"
    if [ -n "$JMX_CONFIG_FILE" ]; then
        JMX_JAVAAGENT_ARG="${JMX_JAVAAGENT_ARG}:${JMX_CONFIG_FILE}" # Añadir : y la ruta del archivo
    else
        JMX_JAVAAGENT_ARG="${JMX_JAVAAGENT_ARG}:" # Si no hay archivo, añadir solo el :
    fi


    # Añadir el argumento del javaagent a KAFKA_OPTS
    if [ -z "$KAFKA_OPTS" ]; then
      export KAFKA_OPTS="$JMX_JAVAAGENT_ARG"
    else
      export KAFKA_OPTS="$KAFKA_OPTS $JMX_JAVAAGENT_ARG" # Añadir un espacio antes por si ya hay opciones
    fi

    echo "DEBUG: JMX Exporter: Configurado en puerto $JMX_PORT para node.id=$NODE_ID." >&2
    echo "DEBUG: JMX Exporter: KAFKA_OPTS resultante: '$KAFKA_OPTS'" >&2
fi

# --- FIN DE MODIFICACIÓN PARA JMX EXPORTER ---
````
Antes de arrancar los servicios del controller y los brokers,necesitamos iniciar Kafka.Por ello vamos a generar un identificador único para el clúster.Este ID se va a utilizar para cada uno de los nodos (controller y brokers)para identificarse como parte del mismo clúster

Generamos el ID del clúster
````
#Generamos un cluster UUID y los IDs de los controllers
KAFKA_CLUSTER_ID="$(/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh random-uuid)"
CONTROLLER_1_UUID="$(/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh random-uuid)"
echo $KAFKA_CLUSTER_ID
````
![image](https://github.com/user-attachments/assets/eb9b2605-8862-43f8-bb7d-7f7c47474a31)

Después de generar el ID ,vamos a formatear los directorios de log de cada nodo.Esto nos va a asegurar que cada nodo este vinculado al mismo cluster.id y pueda participar en la gestión del clúester
````
/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID --standalone -c /opt/kafka/proyecto_MLU/config/controller1.properties
/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c /opt/kafka/proyecto_MLU/config/broker1.properties
/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c /opt/kafka/proyecto_MLU/config/broker2.properties
````
![image](https://github.com/user-attachments/assets/1ab03493-51c0-4fff-aeae-ff9e5e469d62)

Iniciamos los server(1 controller y 2 brokers) cada uno en una terminal distinta

````
#Ejecuta el servidor Kafka
/opt/kafka_2.13-4.0.0/bin/kafka-server-start_proyecto_MLU.sh /opt/kafka/proyecto_MLU/config/controller1.properties
/opt/kafka_2.13-4.0.0/bin/kafka-server-start_proyecto_MLU.sh /opt/kafka/proyecto_MLU/config/broker1.properties
/opt/kafka_2.13-4.0.0/bin/kafka-server-start_proyecto_MLU.sh /opt/kafka/proyecto_MLU/config/broker2.properties
````
### 5.4 Creamos el Topic Kafka
En esta fase,procedemos a la creación del tópico principal de Kafka donde se publicarán todos los eventos generados por nuestro productor de datos en tiempo real.Este tópico se denominará air-quality, ya que su función será centralizar la información relacionada con la calidad del aire, tráfico, incendios y eventos especiales en distintas zonas de la ciudad.

Dado que nuestra simulación abarca cuatro zonas geográficas distintas de Madrid (centro, residencial, industrial y suburbana), decidimos configurar el tópico con 4 particiones, de manera que cada una pueda gestionar de forma paralela y eficiente los eventos específicos de una zona. Esto mejora el rendimiento del sistema,permite mayor paralelización en el consumo de datos y facilita una asignación lógica de responsabilidades entre los consumidores.
Además,se ha definido un factor de replicación de 2,con el objetivo de garantizar una mayor tolerancia a fallos.Esto significa que cada partición estará replicada en al menos dos nodos del clúster, lo cual asegura disponibilidad incluso si uno de los brokers falla.
````
/opt/kafka_2.13-4.0.0/bin/kafka-topics.sh --create --topic air-quality --bootstrap-server 192.168.11.10:9094 --replication-factor 2 --partitions 4
````
Para eliminar el topic si es necesario:
````
/opt/kafka_2.13-4.0.0/bin/kafka-topics.sh --delete --bootstrap-server 192.168.11.10:9094 --topic  air-quality
````
Verificación:
Para comprobar que el tópico ha sido creado correctamente y está activo en nuestro clúster Kafka, usamos:
````
/opt/kafka_2.13-4.0.0/bin/kafka-topics.sh --list --bootstrap-server 192.168.11.10:9094
````
![image](https://github.com/user-attachments/assets/1ae0aafe-e850-437c-a781-9aa21d2dc3ba)


### 5.5 Creación de la tabla en MySQL

Primero, accedemos a la consola de MySQL con privilegios de administrador utilizando el siguiente comando:
````
sudo mysql -u root -p
````
Una vez dentro, creamos una base de datos llamada kafka_air_quality que servirá como contenedor para las tablas relacionadas con nuestro proyecto:
````
CREATE DATABASE kafka_air_quality;
````

![image](https://github.com/user-attachments/assets/38af9f9c-adb3-466c-be61-fb6a4f90ee21)

Dentro de la base de datos, creamos la tabla air_quality_events. Esta tabla almacenará toda la información capturada y procesada, con columnas que representan las diferentes variables de interés, tales como la calidad del aire, conteo de vehículos, presencia de incendios, y más:
````
CREATE TABLE air_quality_events (
    city VARCHAR(100),
    country VARCHAR(100),
    ts VARCHAR(100),
    pollution_aqius INT,
    pollution_mainus VARCHAR(100),
    vehicles_count INT,
    vehicles_passed INT,
    industrial_activity VARCHAR(100),
    fire_active BOOLEAN,
    fire_intensity VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    zone VARCHAR(100),
    traffic_factor FLOAT,
    fire_probability FLOAT,
    industry_factor FLOAT,
    traffic_condition VARCHAR(100),
    special_event VARCHAR(100),
    updated_aqi INT
);
````

![image](https://github.com/user-attachments/assets/112a9eec-10c7-47d0-ae86-0c5d33b21928)


### 5.6 Creación del producer y del consumer

Vamos a crear el productor Kafka que es el componente encargado de simular la generación de datos que normalmente serían capturados por sensores distribuidos en las cuatro zonas de Madrid: centro, residencial, industrial y suburbana.Este productor,implementado en Python,genera eventos sintéticos que incluyen variables como la calidad del aire, el conteo de vehículos, incendios activos y eventos especiales, y los envía en tiempo real al tópico air-quality de Kafka.
Tenemos además varias condiciones para que podemos simular bien nuestros datos y se acerquen lo más posible a la realidad.
Vamos a tener en cuenta esta lógica en la simulación.

* Horario de simulación
El sistema inicia la simulación a las 9:00 de la mañana del día 2 de enero de 2025 que es jueves.Cada segundo en el mundo real representa cinco minutos en el tiempo simulado.

* Condiciones de tráfico
Las condiciones del tráfico son un factor importante para el cálculo del AQI (índice de calidad del aire).Se tienen en cuenta dos aspectos principales: el día de la semana y la hora del día.

Durante los días de semana,se considera que hay horas punta (a las 8, 9, 14, 15 y 20 horas), donde hay más tráfico en el centro de la ciudad. Durante los fines de semana,el tráfico disminuye.Si el momento actual de la simulación coincide con una hora punta , se clasifica como condición de tráfico “peak”, si es fin de semana, se clasifica como “weekend”, y en los demás casos como “normal”.

Cada zona dispone de diferentes condiciones.Por ejemplo,en el centro de Madrid se registra un mayor número de vehículos durante las horas punta,mientras que en zonas suburbanas la variación es mínima.

* Factor industrial
En las zonas industriales,este factor tiene una influencia mucho mayor.En estas áreas donde se concentra la mayor emisión de contaminantes debido a la actividad de las fábricas y procesos industriales. Por lo tanto, son las zonas donde más se notará el impacto en la calidad del aire.

* Incendios forestales 
Los incendios son otro factor muy importante en esta simulación.Cada zona tiene asignada una probabilidad específica de que ocurra un incendio.Por ejemplo,en las zonas suburbanas es más probable que se origine un incendio.

* Eventos especiales
Solo en la zona del centro se simulan eventos especiales como conciertos y partidos de fútbol. Cuando ocurre uno de estos eventos,se incrementa el número de vehículos en la zona y se eleva el AQI debido al aumento del tráfico.

Déspues necesitamos un consumer que lea los eventos del topic air-quality.Este consumer está implementado en PySpark Structured Streaming para poder analizar los datos de forma continua y reactiva.
El consumer :
Lee el flujo de mensajes desde Kafka.
Extrae y estructura los datos JSON recibidos.
Imprime un resumen por microbatch en consola.
Para facilitar la conexión con Power BI,además de almacenar los datos en HDFS,hemos creado una tabla en MySQL.Esto nos permite guardar y actualizar los datos generados de forma más sencilla y accesible para herramientas de análisis.

#### 5.6.1 Ejecutamos el Consumer

Es fundamental iniciar el consumidor antes de poner en marcha el productor.Esto asegura que el consumer esté activo desde el inicio del flujo de datos y no se pierda ninguna información emitida por el productor.
Para ejecutar el consumidor utilizamos spark-submit con las librerías necesarias para conectar Spark con Kafka. El comando es el siguiente:

````
PYTHONPATH=$HOME/.local/lib/python3.10/site-packages spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 --master spark://192.168.11.10:7077 /opt/kafka/proyecto_MLU/data_stream/consumer.py
````
#### 5.6.2 Ejecutamos el Producer Kafka

Una vez que el consumidor está corriendo y escuchando el stream, procedemos a iniciar el productor.El producer simula la generación y envío de datos sintéticos desde las distintas zonas de la ciudad, alimentando el flujo que será consumido y analizado.
Para lanzar el productor ejecutamos:
````
python3 /opt/kafka/proyecto_MLU/data_stream/producer.py
````
Este script comenzará a enviar los eventos generados al topic Kafka,dando inicio a la simulación y procesamiento de datos.

#### 5.6.3 Visualizamos la información

Para asegurarnos de que los datos se están consumiendo correctamente y el flujo de información está activo, utilizaremos la Consumer API de Kafka para monitorear el consumo en tiempo real. Ejecutamos el siguiente comando para ver los mensajes que llegan al topic air-quality desde el principio:
````
/opt/kafka_2.13-4.0.0/bin/kafka-console-consumer.sh --topic air-quality --from-beginning --bootstrap-server 192.168.11.10:9094
````
Este comando mostrará en la consola los eventos que el consumidor está recibiendo, permitiendo verificar que los datos fluyen correctamente.

Además, para comprobar que los datos se están almacenando correctamente en el sistema de archivos distribuido HDFS, podemos listar los archivos generados con:

````
hdfs dfs -ls /opt/kafka/proyecto_MLU/data/
````
![image](https://github.com/user-attachments/assets/baca4845-0b2b-4fcb-9ee1-004e7e53dcd1)

* Visualización web del sistema de archivos HDFS:

También podemos acceder a la interfaz web de HDFS para una visualización más amigable de los archivos y directorios:

http://192.168.56.10:9870/explorer.html

![image](https://github.com/user-attachments/assets/eb74a8c9-18de-4be6-85c3-ced1ca068ade)

* Visualizamos que los datos se han guardado en nuestra base de datos de Mysql 
Finalmente, verificamos que los datos se hayan insertado correctamente en la base de datos MySQL, donde se almacenan para facilitar su análisis y conexión con herramientas como Power BI.

![image](https://github.com/user-attachments/assets/39c16059-7e8e-44f0-ba78-a850521f9fe3)


## 6. Visualización en PowerBI
En este apartado,abordaremos el proceso para conectar con PowerBI con nuestra base de datos MYSQL con el fin de realizar un análisis visual dinámico de los datos almacenados.

* Conexión de PowerBI con la base de datos MYSQL
Para comenzar abrimos PowerBI y seleccionamos la opción de conectamos a una base de datos MySQL.Esta conexión nos permitirá extraer los datos necesarios directamente desde nuestra base,asegurando que los informes reflejen siempre la información más reciente.

![image](https://github.com/user-attachments/assets/db769c6b-aeda-4546-96c7-e8ee26775ad9)

* Introducimos nuestra IP donde se encuentra alojada nuestra base de datos MYSQL ,así como el nombre  específico de nuestra base de datos que queremos consultar.Además tendremos que introducir nuestro usuario y contraseña.

![image](https://github.com/user-attachments/assets/03825a69-aae7-4101-bef5-f0def19f6b8a)

### 6.1 Promedio de AQI

![image](https://github.com/user-attachments/assets/544aaaba-3959-4da6-853d-dd6b1b6088a7)

````
AQI Promedio por Zona = 
AVERAGEX(
    VALUES('kafka_air_quality air_quality_events'[zone]),
    CALCULATE(AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]))
)
````

## 1. Descripción
Se presentan los datos sobre el Índice de Calidad del Aire (AQI) promedio y su distribución porcentual en cuatro zonas distintas de Madrid.

## 2. Datos Generales
El análisis muestra las diferencias en la calidad del aire entre las zonas monitoreadas:
- Las zonas **industrial** y **centro** concentran aproximadamente el 66.45% 
- La zona **residencial** contribuye con el 14.68% del AQI total.
- La zona **suburbana** muestra el menor impacto.

## 3. Distribución de Contaminación por Zona
Los datos muestran cómo los factores urbanos e industriales afectan más a la calidad del aire:
- **Zona Industrial (33.25%): Presenta los valores más altos,vinculados a la actividad fabril y emisiones industriales.
- **Centro (33.2%): Muestra niveles similares a la zona industrial,vinculados al intenso tráfico  y alta densidad urbana.
- **Residencial (14.68%): Exhibe niveles moderados, reflejando menor actividad contaminante pero aún afectada por el entorno urbano.
- **Suburbana : Registra la mejor calidad de aire,beneficiada por menor densidad poblacional y mayor presencia de áreas verdes.

## 4. Interpretación de Resultados

Los datos confirman:

1. **Actividad humana**: Las zonas industrial y centro tienen peor calidad del aire por fábricas y tráfico.
2. **Tráfico**: El centro esta casi tan contaminado como la zona industrial.
3. **Planeación urbana**: La zona residencial tiene mejor aire..
4. **Zonas alejadas**: La suburbana tiene el mejor aire gracias a menos población y más naturaleza.

### 5.Conclusiones

* Reducir el tráfico en el centro.
* Cuidar la calidad del aire en zonas residenciales.
* Proteger las zonas suburbanas como espacios verdes.


### 6.2 Análisis de Calidad del Aire (AQI) en Zonas Industriales

![image](https://github.com/user-attachments/assets/1e0466c1-0bd8-4bcd-b98e-ed48cce9cc14)

````
Avg AQI Con Fuego = 
CALCULATE(
    AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]),
    'kafka_air_quality air_quality_events'[fire_active] = TRUE(),
    'kafka_air_quality air_quality_events'[zone] = "suburb"
)
````
````
Avg AQI Sin Fuego = 
CALCULATE(
    AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]),
    'kafka_air_quality air_quality_events'[fire_active] = FALSE(),
    'kafka_air_quality air_quality_events'[zone] = "suburb"
)
````

## 1. Descripción
Este gráfico presenta tres métricas clave de calidad del aire (AQI) específicamente relacionadas con zonas industriales: AQI Alta Industria, AQI Baja Industria y AQI Media Industria, desglosadas por diferentes zonas urbanas.

## 2. Datos Generales
El análisis muestra cómo varía el impacto industrial en la calidad del aire según la zona:
- Se comparan tres indicadores de contaminación industrial (alta, baja y media)

## 3. Distribución del AQI Industrial por Zona

### **Zona Industrial**
- Muestra los valores más altos en **AQI Alta Industria** y confirma  el fuerte impacto de la actividad fabril

### **Centro**
- Registra valores intermedios de **AQI Media Industria**, sugiere que hay menos actividad industrial

### **Zona Residencial**
- Exhibe valores moderados en **AQI Baja Industria**, pero con presencia detectable

### **Zona Suburbana**
- Muestra los valores más bajos en los tres indicadores

## 4. Interpretación de Resultados

**Impacto geográfico de la industria**: La contaminación industrial no se limita a su zona de origen,sino que se extiende a áreas vecinas por los vientos.

## 5. Conclusiones 
  - Se podría monitorear las zonas aledañas a polos industriales
  - Regular  los horarios de máxima producción contaminante
  - Mantener suficiente distancia entre zonas industriales y residenciales
  - Considerar patrones de viento predominantes en la planificación urbana


### 6.3 Análisis del Impacto de Incendios en la Calidad del Aire (AQI) en Zona Suburbana

![image](https://github.com/user-attachments/assets/ffcc1651-a7e6-4f4f-8319-a426d9596614)

## 1. Descripción
Este gráfico compara el Índice de Calidad del Aire (AQI) promedio en la zona suburbana en dos escenarios distintos: cuando no hay incendios activos (Avg AQI Sin Fuego) y cuando existen incendios forestales (Avg AQI Con Fuego).

## 2. Datos Clave
- **AQI Sin Fuego**: Muestra la calidad del aire base en condiciones normales
- **AQI Con Fuego**: Refleja el deterioro de la calidad del aire durante incendios forestales

## 3. Hallazgos Principales

### **Condiciones Normales (Sin Fuego)**
- La zona suburbana mantiene un AQI bajo cuando no hay  incendios
- Corresponde a los valores más saludables del sistema de monitoreo

### **Durante Incendios (Con Fuego)**
- Se observa un incremento significativo del AQI
- El aumento puede ser de 5 a 10 veces el valor base según la  intensidad del fuego

## 4. Interpretación
 Aunque normalmente es la zona con mejor aire,la suburbana es la más afectada durante incendios forestales.
 Los incendios pueden causar un  deterioro rápido y severo de la calidad del aire y puede transformar  el área suburbana en la más contaminada.

## 5. Conclusión
Se podría implementar protocolos específicos para incendios en áreas suburbanas
Poner más sensores durante la temporada de incendios

### 6.4 Promedio de Vehículos por Minuto y AQI por Zona

````
Avg Vehiculo Por Minuto = AVERAGEX(
    VALUES('kafka_air_quality air_quality_events'[ts]),
    CALCULATE(AVERAGE('kafka_air_quality air_quality_events'[vehicles_passed]))
)
````
````
AQI Promedio por Zona = 
AVERAGEX(
    VALUES('kafka_air_quality air_quality_events'[zone]),
    CALCULATE(AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]))
)
````

### 1. Descripción General  
El gráfico muestra dos métricas clave para cuatro zonas distintas (center, residential, suburb,industrial):  
- **Avg Vehículo Por Minuto**: Número promedio de vehículos que transitan por minuto.  
- **AOI Promedio por Zona**: Índice de Calidad del Aire (AQI) promedio en cada zona

---

### 2. Datos Clvae
- **Zona center:  
  - Como podemos ver a partir de la 9:00,14:00,15:00,20:00 horas el AQI sube considerablemente a 200 y la media de coches por minuto incrementa también 
 
   ![image](https://github.com/user-attachments/assets/8765ecf5-cf39-4ea5-84a0-753ef89f4658)
 

- **Zonas residential
  En el caso de la zona residencial el nivel de AQI se mantiene constante durante practicamente todo el dia 

  ![image](https://github.com/user-attachments/assets/6aced553-6157-472b-a6f5-2c640d33d8e5)
 
- **Zonas suburbana
  En la zona suburbana,se observa que el tráfico muy bajo ,pero existen picos de AQI .
  La posible causa principal puede ser los incendios forestales o agrícolas cercanos ya que no coincide con aumentos de tráfico y es un fenómeno temporal.

 ![image](https://github.com/user-attachments/assets/cafbdca9-5887-4f9b-a82f-d55783fa4fbb)

- **Zonas industriales
  En zonas industriales se observa un incremento del AQI durante el horario laboral (de 9:00 a 13:00 horas),lo que sugiere una correlación directa entre la actividad industrial y la contaminación del aire.

 ![image](https://github.com/user-attachments/assets/9575f8ef-099c-4694-ba67-dd5150ceddc5)

---

![image](https://github.com/user-attachments/assets/ba3605f6-c018-4555-ab64-de2be18b5f09)


### 6.5 Distribución del AQI por Día de la Semana


![image](https://github.com/user-attachments/assets/d884f5c0-cead-4001-9309-25247056d76c)

Creamos una nueva columna
````
Día de la semana = 
VAR FechaConvertida = DATEVALUE(LEFT([ts], 10)) // Convierte solo la parte de fecha
VAR FechaBase = DATE(YEAR(FechaConvertida), 1, 2) // 2 de enero del mismo año
VAR DiasDiferencia = DATEDIFF(FechaBase, FechaConvertida, DAY)
VAR DiaSemanaNum = MOD(DiasDiferencia + 4, 7) + 1
RETURN
SWITCH(
    DiaSemanaNum,
    1, "Domingo",
    2, "Lunes",
    3, "Martes",
    4, "Miércoles",
    5, "Jueves",
    6, "Viernes",
    7, "Sábado",
    "Desconocido"
)
````

````
AQI Promedio por Zona = 
AVERAGEX(
    VALUES('kafka_air_quality air_quality_events'[zone]),
    CALCULATE(AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]))
)
````
1. Descripción General
El gráfico generado muestra cómo varía el promedio del Índice de Calidad del Aire (AQI) a lo largo de los días de la semana .
Esto permite identificar posibles patrones de contaminación asociados a la actividad humana y la dinámica urbana durante la semana.

2. Datos Clave
Se observa que los niveles de AQI aumentan significativamente durante los días laborales.Esto se debe al incremento de tráfico y a la actividad comercial en el centro urbano.
Los domingos  y los sábados tienden a mostrar valores notablemente más bajos,lo que refuerza la hipótesis del impacto del tráfico.

## 7. Prometheus

En esta etapa, ponemos en marcha Prometheus para comenzar a recolectar métricas de nuestras fuentes configuradas.

1.Iniciar Prometheus

Vamos a su directorio ````/opt/prometheus-2.53.4 ````

Luego, arrancamos Prometheus usando nuestro archivo de configuración personalizado:
````
./prometheus --config.file=prometheus_proyecto_MLU.yml
````
2. Verificar Endpoints de Métricas
   
Una vez iniciado, comprobamos que nuestros endpoints están sirviendo correctamente las métricas:
````
curl http://localhost:11001/metrics
curl http://localhost:11002/metrics
curl http://localhost:11003/metrics
````
3. Confirmar Captura de Prometheus
   
Desde el navegador del host , accedemos a la interfaz de Prometheus:

````http://192.168.56.10:9090/targets````

4. Visualización
   
Las siguientes imágenes muestran la interfaz de Prometheus funcionando correctamente, con los targets en estado activo ("UP"):

![image](https://github.com/user-attachments/assets/f661253c-c5f8-4228-8281-1dbf0f7d63a1)


![image](https://github.com/user-attachments/assets/d1eae758-eb03-4b81-be8c-effd0fe766f9)


## 8. Grafana

En este apartado instalamos y configuramos Grafana, la herramienta de visualización de métricas que se integra con Prometheus.

1. Instalación de Dependencias
   
Primero, instalamos los paquetes necesarios para que Grafana funcione correctamente:
````
sudo apt-get install -y adduser libfontconfig1 musl
````
2. Descargar e Instalar Grafana Enterprise
   
Descargamos el paquete .deb de Grafana Enterprise versión 12.0.1:
````
wget https://dl.grafana.com/enterprise/release/grafana-enterprise_12.0.1_amd64.deb
````
Instalamos el paquete:
````
sudo dpkg -i grafana-enterprise_12.0.1_amd64.deb
````
Esto instalará Grafana como un servicio del sistema.

![image](https://github.com/user-attachments/assets/82de1195-7d43-45f6-b290-cdba015fd09c)

3. Iniciar y Habilitar el Servicio
   
Recargamos los servicios del sistema y configuramos Grafana para que inicie automáticamente con el sistema:
````

sudo systemctl daemon-reload
sudo systemctl enable grafana-server.service
sudo systemctl start grafana-server.service
sudo systemctl status grafana-server.service

 systemctl start grafana-server
````

![image](https://github.com/user-attachments/assets/c32af78e-fbf2-494e-8795-423c7919bf4c)

4. Acceso a la Interfaz Web
   
Una vez iniciado el servicio, accedemos a Grafana desde el navegador web:
````
http://192.168.56.10:3000/dashboards
````
5. Visualización y Paneles
   
Al ingresar por primera vez, Grafana solicitará iniciar sesión (usuario: admin, contraseña por defecto: admin, luego pedirá cambiarla). Desde ahí, se pueden:

Crear dashboards personalizados.

Agregar Prometheus como fuente de datos.

Visualizar las métricas capturadas de forma gráfica.

Aquí vemos capturas del panel de control y algunos ejemplos de dashboards en funcionamiento:

![image](https://github.com/user-attachments/assets/fcf68def-b75a-40c5-adc7-cb9c5bd19d7d)

![image](https://github.com/user-attachments/assets/96508635-e8fa-4291-ba1f-1cd905c7d106)






























