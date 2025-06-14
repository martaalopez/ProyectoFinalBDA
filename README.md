# Proyecto Final BDA 2024-25

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
   - [5.5 Creación del producer y del consumer](#55-creación-del-producer-y-del-consumer)
     - [5.5.1 Ejecutamos el Consumer](#551-ejecutamos-el-consumer)
     - [5.5.2 Ejecutamos el Producer Kafka](#552-ejecutamos-el-producer-kafka)
     - [5.5.3 Visualizamos la información](#553-visualizamos-la-información)
6. [Visualización en PowerBI](#6-visualización-en-powerbi)
   - [6.1 Promedio de AQI](#61-promedio-de-aqi)
   - [6.2 Análisis de Calidad del Aire (AQI) con factor industrial](#62-análisis-de-calidad-del-aire-aqi-con-factor-industrial)
   - [6.3 Análisis del Impacto de Incendios en la Calidad del Aire](#63-análisis-del-impacto-de-incendios-en-la-calidad-del-aire-aqi-en-zona-suburbana)
   - [6.4 Promedio de Vehículos por Minuto y AQI por Zona](#64-promedio-de-vehículos-por-minuto-y-aqi-por-zona)
   - [6.5 Distribución del AQI por Día de la Semana](#65-distribución-del-aqi-por-día-de-la-semana)
7. [Prometheus](#7-prometheus)
8. [Grafana](#8-grafana)


## 1. Introducción

Hoy en día, la calidad del aire y la contaminación son factores ambientales que generan gran preocupación en nuestra sociedad.
El tráfico diario de vehículos es una de las principales causas del deterioro de la calidad del aire.
Además, ciertos fenómenos naturales como los incendios forestales pueden tener un impacto significativo en la contaminación atmosférica. A esto se le suma la actividad industrial, cuyas emisiones de humo y partículas contaminantes se mezclan con la atmósfera, empeorando aún más la situación.

Esto puede hacer que existan consecuencias directas en la salud pública, un artículo revela que 2000 niños mueren cada dia en el mundo por mal calidad del aire, por ello he decidido hacer una investigación que se enfoca en el monitoreo y análisis de los principales factores que afectan la calidad del aire, con el objetivo de identificar los eventos más frecuentes y críticos.A partir de estos datos, espero poder extraer conclusiones que contribuyan a diseñar soluciones eficientes para combatir este grave problema global.
  

## 2. Fuente de Información

Para poder abarcar con todo esto vamos a apoyarnos en los datos proporcionados por la AirVisual API la cual ofrece información sobre el tiempo, la calidad del aire y los incendios activos,etc...
Sin embargo, esta API presenta un problema: los datos se actualizan cada hora , mientras que nuestro objetivo es realizar un monitoreo en tiempo real, actualizando los datos cada segundo.

Por ello vamos a generar unos datos sintéticos, incluyendo no solo las variables que ofrece la API, sino también otros datos adicionales que considero importantes para un análisis más completo, como el tráfico, la actividad industrial y la probabilidad de incendios.
Los datos ficticios se recogerán desde sensores virtuales distribuidos en cuatro zonas distintas de Madrid:

Centro: La cual va a tener un alto volumen de tráfico.

Residencial: Es un área más residencial con menos tráfico de vehículos.

Industrial: Es una zona con alta actividad industrial,donde predominan los contaminantes derivados del humo y procesos fabriles.

Suburbana: Es una zona de factores naturales y con una mayor probabilidad de incendios forestales.

## 3. Requisitos
Debe haber como mínimo 3 nodos en los clusters (en cada uno):

* Hadoop (HDFS/Yarn)
 Hadoop es el sistema responsable del almacenamiento distribuido de grandes volúmenes de datos (HDFS) y de la gestión de recursos y ejecución de tareas distribuidas (YARN).
 ![image](https://github.com/user-attachments/assets/bbe8c104-5059-4658-88ab-952a1f15c1cb)
 
 ![image](https://github.com/user-attachments/assets/ee90e9d2-2931-43d7-b1bb-297e8eb30cb9)


* Spark
 Apache Spark es el motor encargado del procesamiento distribuido de los datos. A diferencia de Hadoop MapReduce, Spark nos permite trabajar en memoria, lo que lo hace mucho más rápido y eficiente para el análisis de grandes volúmenes de datos.
 
 ![image](https://github.com/user-attachments/assets/4a360f4a-3007-4646-92e2-289e0c5d676c)


* Kafka
 Apache Kafka es la tecnología utilizada para gestionar el flujo de mensajes en tiempo real. En este proyecto , Kafka se encarga de transmitir los eventos generados por los sensores virtuales (como los datos de calidad del aire, tráfico, incendios, etc.).
 Se ha actualizado Kafka a la versión 4.0.0, lo que introduce una mejora importante: la eliminación de la dependencia de Zookeeper, gracias al nuevo sistema de metadatos KRaft.
 
 ![image](https://github.com/user-attachments/assets/1d2feb40-6772-4ea7-9e3f-e7edf1420f69)


## 4. Configuración del Clúster de Kafka
1.Vamos a establecer todos los archivos de configuración en una carpeta llamada proyecto_MLU, que en mi caso estará alojada en /opt/kafka/proyecto_MLU

![image](https://github.com/user-attachments/assets/e12ef486-f0bd-4ca7-b4fa-3a83788f20b7)

Creamos los directorios necesarios para nuestro proyecto_MLU

````
mkdir -p /opt/kafka/proyecto_MLU/config
mkdir -p /opt/kafka/proyecto_MLU/logs
````

En nuestra arquitectura vamos a tener lo siguiente:
Un controller que va a ser el nodo responsable de poder coordinar el clúster. Se va a encargar de gestionar los eventos como la creación y eliminación de topics,la asignación de particiones y la detección de fallos en los brokers.
Para el controller, debemos usar como base la configuración de propiedades de controller de kafka que se encuentran :
````
config/controller.properties
````
Dos brokers, donde cada uno va a estar identificado por un Id y va a contener ciertas particiones de un topic.Va a permitir replicar y poder particionar dichos topics balanceando la carga de almacenamiento entre los brokers.
Para cada broker, necesitaremos crear un archivo de configuración por separado.Para ello debemos usar como base la configuración de propiedades de brokers de kafka que se encuentran 

````
config//broker.properties
````
Hacemos la copia de los ficheros correspondientes de configuración para cada uno

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
Levantamos HDFS que será nuestro sistema de almacenamiento distribuido, donde los datos procesados se guardarán.
Se inician los servicios del NameNode y los DataNodes, permitiendo el almacenamiento distribuido de grandes volúmenes de datos.
Se activa YARN, que gestionará los recursos y la ejecución de procesos en los distintos nodos del clúster.
Esto asegura que todo lo que se procese o almacene posteriormente tenga soporte escalable y tolerante a fallos.
````
cd $HADOOP_HOME
stop-dfs.sh
start-dfs.sh
stop-yarn.sh
start-yarn.sh

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
Como más adelante utilizaremos Prometheus y Grafana, se ha preparado un script personalizado llamado kafka-server-start_proyecto_MLU.sh adaptado especialmente para este proyecto.

1.Configurar Prometheus
Tras a ver instalado prometheus, duplicamos el archivo de configuración por defecto y creamos uno específico para el proyecto.
Este script está diseñado para poder iniciar instancias de Kafka personalizadas para el proyecto, específicamente configuradas para que cada broker y controller de Kafka use un puerto diferente , asi evitamos errores de conflictor de red  y monitoreo al ejecutar múltiples nodos Kafka en la misma máquina.
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
En este script vamos a crear una configuración adicional para habilitar JMX Exporter, lo que permitirá monitorear los nodos de Kafka con Prometheus.
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
Antes de arrancar los servicios del controller y los brokers, necesitamos iniciar Kafka. Por ello vamos a generar un identificador único para el clúster. Este ID se va a utilizar para cada uno de los nodos (controller y brokers) para identificarse como parte del mismo clúster

Generamos el ID del clúster
````
#Generamos un cluster UUID y los IDs de los controllers
KAFKA_CLUSTER_ID="$(/opt/kafka_2.13-4.0.0/bin/kafka-storage.sh random-uuid)"
echo $KAFKA_CLUSTER_ID
````
![image](https://github.com/user-attachments/assets/eb9b2605-8862-43f8-bb7d-7f7c47474a31)

Después de generar el ID , vamos a formatear los directorios de log de cada nodo. Esto nos va a asegurar que cada nodo este vinculado al mismo cluster.id y pueda participar en la gestión del clúster
Ponemos --standalone al iniciar el controller ya que se usa en la version 4 para  poder formatear el nodo que actuará solo como controller KRaft.
Los brokers no deben usar --standalone, a menos que sean solo controllers, lo cual no es típico.
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
En esta fase, procedemos a la creación del tópico principal de Kafka donde se publicarán todos los eventos generados por nuestro productor de datos en tiempo real. Este tópico se denominará air-quality, su función será reunir la información relacionada con la calidad del aire, tráfico, incendios y eventos especiales en distintas zonas de la ciudad.

Dado que nuestra simulación abarca cuatro zonas geográficas distintas de Madrid (centro, residencial, industrial y suburbana), decidimos configurar el tópico con 4 particiones, de manera que cada una pueda gestionar de forma paralela y eficiente los eventos específicos de una zona. Esto va a mejorar el rendimiento del sistema y permite mayor paralelización en el consumo de datos.
Además, se ha definido un factor de replicación de 2, con el objetivo de garantizar una mayor tolerancia a fallos. Esto significa que cada partición estará replicada en al menos dos nodos del clúster, lo cual asegura disponibilidad incluso si uno de los brokers falla.
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


### 5.5 Creación del producer y del consumer

Vamos a crear el productor Kafka que es el componente encargado de simular la generación de datos que normalmente serían capturados por sensores distribuidos en las cuatro zonas de Madrid: centro, residencial, industrial y suburbana. Este productor, implementado en Python, genera eventos sintéticos que incluyen variables como la calidad del aire, el conteo de vehículos,incendios activos y eventos especiales, y los envía en tiempo real al tópico air-quality de Kafka.
Tenemos además varias condiciones para que podemos simular bien nuestros datos y se acerquen lo más posible a la realidad.
Vamos a tener en cuenta esta lógica en la simulación.

* Horario de simulación
El sistema inicia la simulación a las 9:00 de la mañana del día 2 de enero de 2025 que es jueves. Cada segundo en el mundo real representa cinco minutos en el tiempo simulado.

* Condiciones de tráfico
Las condiciones del tráfico son un factor importante para el cálculo del AQI. Se tienen en cuenta dos aspectos principales:el día de la semana y la hora del día.

Durante los días de semana, se considera que hay horas punta (a las 9, 14, 15 y 20 horas), donde hay más tráfico en el centro de la ciudad. Durante los fines de semana, el tráfico disminuye. Si el momento actual de la simulación coincide con una hora punta, se clasifica como condición de tráfico “peak”,si es fin de semana, se clasifica como “weekend” y en los demás casos como “normal”.

Cada zona dispone de diferentes condiciones. Por ejemplo, en el centro de Madrid se registra un mayor número de vehículos durante las horas punta, mientras que en zonas suburbanas la variación es mínima.

* Factor industrial
En las zonas industriales, este factor tiene una influencia mucho mayor.En estas áreas donde se concentra la mayor emisión de contaminantes debido a la actividad de las fábricas y procesos industriales. Por lo tanto, son las zonas donde más se notará el impacto en la calidad del aire.

* Incendios forestales 
Los incendios son otro factor muy importante en esta simulación. Cada zona tiene asignada una probabilidad específica de que ocurra un incendio. Por ejemplo, en las zonas suburbanas es más probable que se origine un incendio.

* Eventos especiales
Solo en la zona del centro se simulan los eventos especiales como conciertos y partidos de fútbol. Cuando ocurre uno de estos eventos, se incrementa el número de vehículos en la zona y se eleva el AQI debido al aumento del tráfico.

Después necesitamos un consumer que lea los eventos del topic air-quality. Este consumer está implementado en PySpark Structured Streaming para poder analizar los datos de forma continua.
El consumer :

Va a leer el flujo de mensajes desde Kafka.

Extrae y estructura los datos JSON recibidos.

Imprime un resumen por microbatch en consola.

### 5.5.1 Ejecutamos el Consumer

Vamos a iniciar el consumidor antes de poner en marcha el productor. Esto va a asegurar que el consumer esté activo desde el inicio del flujo de datos y no se pierda ninguna información emitida por el productor.
Para ejecutar el consumidor utilizamos spark-submit con las librerías necesarias para conectar Spark con Kafka. El comando es el siguiente:

````
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 --master spark://192.168.11.10:7077 /opt/kafka/proyecto_MLU/data_stream/consumer.py
````
### 5.5.2 Ejecutamos el Producer Kafka

Una vez que el consumidor está corriendo y escuchando el stream, vamos a proceder a iniciar el productor.El producer simula la generación y envío de datos sintéticos desde las distintas zonas de la ciudad,alimentando el flujo que será consumido y analizado.
Para lanzar el productor ejecutamos:
````
python3 /opt/kafka/proyecto_MLU/data_stream/producer.py
````
Este script comenzará a enviar los eventos generados al topic Kafka,dando inicio a la simulación y procesamiento de datos.

### 5.5.3 Visualizamos la información

Para asegurarnos de que los datos se están consumiendo correctamente y el flujo de información está activo,utilizaremos la consumer API de Kafka para monitorear el consumo en tiempo real. Ejecutamos el siguiente comando para ver los mensajes que llegan al topic air-quality desde el principio:
````
/opt/kafka_2.13-4.0.0/bin/kafka-console-consumer.sh --topic air-quality --from-beginning --bootstrap-server 192.168.11.10:9094
````
Este comando mostrará en la consola los eventos que el consumidor está recibiendo, permitiendo verificar que los datos fluyen correctamente.

Además, para comprobar que los datos se están almacenando correctamente en el sistema de archivos distribuido HDFS,podemos listar los archivos generados con:

````
hdfs dfs -ls /opt/kafka/proyecto_MLU/data/
````
![image](https://github.com/user-attachments/assets/baca4845-0b2b-4fcb-9ee1-004e7e53dcd1)

* Visualización web del sistema de archivos HDFS:

También podemos acceder a la interfaz web de HDFS para visualizar los archivos y directorios:

http://192.168.56.10:9870/explorer.html

![image](https://github.com/user-attachments/assets/eb74a8c9-18de-4be6-85c3-ced1ca068ade)

* Visualizamos que los datos se han guardado en nuestra base de datos de Mysql 
Finalmente,verificamos que los datos se hayan insertado correctamente en la base de datos MySQL,donde se almacenan para facilitar su análisis y conexión con herramientas como Power BI.

![image](https://github.com/user-attachments/assets/39c16059-7e8e-44f0-ba78-a850521f9fe3)


## 6. Visualización en PowerBI
En esta sección, explicaremos paso a paso cómo conectar Power BI con un sistema de archivos distribuido HDFS, con el objetivo de realizar análisis visuales dinámicos de los datos almacenados en Hadoop.
Antes de realizar la conexión, es necesario configurar correctamente el archivo hosts de nuestro sistema operativo para que Power BI pueda resolver los nombres de los nodos del clúster Hadoop.

1.Abrimos primero el archivo hosts en nuestro equipo.:

![image](https://github.com/user-attachments/assets/92c1904f-12b0-4d42-8ea9-9236bb695cc9)

2.Editamos el archivo como administrador y añadimos las siguientes líneas al final:
````
# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1             localhost
# Added by Docker Desktop
192.168.1.37 host.docker.internal
192.168.1.37 gateway.docker.internal
# To allow the same kube context to work on the host and the container:
127.0.0.1 kubernetes.docker.internal
# End of section

192.168.56.10 master
192.168.56.11 nodo1
192.168.56.12 nodo2
192.168.56.13 nodo3
````

Una vez configurado el archivo hosts, podemos proceder a conectar Power BI con HDFS y visualizar nuestros datos.
1. Abrir Power BI

Iniciamos Power BI Desktop.

2. Conectarse a Hadoop HDFS
   
En la pantalla de inicio, seleccionamos Obtener datos.

Buscamos y seleccionamos la opción Archivo Hadoop (HDFS).

![image](https://github.com/user-attachments/assets/d8f298e5-ad49-4677-a4a6-6c48af2b9be8)

3. Introducir la dirección del servidor

En la ventana emergente, introducimos la dirección del nodo principal  donde se aloja el sistema de archivos HDFS.

![image](https://github.com/user-attachments/assets/24de34b3-bfd8-4e52-afd4-f02b0153eab2)

4. Transformar los datos
   
Una vez conectado, Power BI mostrará los archivos disponibles .A continuación, realizamos los siguientes pasos:

Hacemos clic en Transformar datos para abrir el Editor de Power Query.
![image](https://github.com/user-attachments/assets/bb8b2d03-d4cd-46e5-9002-6b119bc97f70)

5. Seleccionar formato de archivo

En la columna Extension, seleccionamos el formato de archivo adecuado, que sería en nuestro caso .parquet.

![image](https://github.com/user-attachments/assets/453a7bee-ee64-4a70-a242-31af6c148070)

6. Abrir archivo binario

Hacemos clic sobre el campo Binary del archivo que deseamos cargar.

![image](https://github.com/user-attachments/assets/f5f31d7c-1035-413e-a407-be4df04f9a26)

7. Aplicar cambios

Una vez que Power BI haya creado la consulta y cargado los datos, hacemos clic en Cerrar y aplicar.

![image](https://github.com/user-attachments/assets/0b5947b2-b602-4306-aa2a-0885f6cfc504)

Ya tenemos nuestros datos preparados

![image](https://github.com/user-attachments/assets/43b47665-2475-4ef1-9573-477f8540289a)


### 6.1 Promedio de AQI

![image](https://github.com/user-attachments/assets/544aaaba-3959-4da6-853d-dd6b1b6088a7)

Creamos una nueva medida
````
AQI Promedio por Zona = 
AVERAGEX(
    VALUES('kafka_air_quality air_quality_events'[zone]),
    CALCULATE(AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]))
)
````
Aplicamos la función AVERAGEX para recorrer cada zona única (VALUES) y calcular el promedio de pollution_aqius (Air Quality Index US) mediante CALCULATE.

### 1. Descripción
Vamos a presentar el promedio del índice de Calidad del Aire (AQI)  y su distribución porcentual en cuatro zonas distintas de Madrid.

### 2. Datos Generales
El análisis muestra las diferencias en la calidad del aire entre las zonas monitoreadas:
- Las zonas **industrial** y **centro** concentran aproximadamente el 66.45% 
- La zona **residencial** contribuye con el 14.68% del AQI total.
- La zona **suburbana** muestra el menor impacto.

### 3. Distribución de Contaminación por Zona
Los datos muestran cómo los factores urbanos e industriales afectan más a la calidad del aire:
- Zona Industrial (33.25%):Presenta los valores más altos,vinculados a la actividad fabril y emisiones industriales.
- Centro (33.2%):Muestra niveles similares a la zona industrial,vinculados al intenso tráfico  y alta densidad urbana.
- Residencial (14.68%):Exhibe niveles moderados,reflejando menor actividad contaminante pero aún afectada por el entorno urbano.
- Suburbana :Registra la mejor calidad de aire,beneficiada por menor densidad poblacional y mayor presencia de áreas verdes.

### 4. Interpretación de Resultados

Como podemos observar

1. Las zonas industrial y centro tienen peor calidad del aire por fábricas y tráfico.
2. El centro esta casi tan contaminado como la zona industrial.
3. La zona residencial tiene mejor aire.
4. La suburbana tiene el mejor aire gracias a menos población y más naturaleza.

### 5.Conclusiones

* Se podría reducir el tráfico en el centro.
* Cuidar la calidad del aire en zonas residenciales,donde viven más personas
* Proteger las zonas suburbanas como espacios verdes.


### 6.2 Análisis de Calidad del Aire (AQI) con factor industrial

![image](https://github.com/user-attachments/assets/1e0466c1-0bd8-4bcd-b98e-ed48cce9cc14)


Para segmentar el análisis, se generaron tres medidas en DAX que calculan el promedio del AQI para cada nivel de actividad industrial:

````
AQI Alta Industria = 
CALCULATE(
    AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]),
    'kafka_air_quality air_quality_events'[industrial_activity] = "high"
)

````
````
AQI Baja Industria = 
CALCULATE(
    AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]),
    'kafka_air_quality air_quality_events'[industrial_activity] = "low"
)
````
````
AQI Media Industria = 
CALCULATE(
    AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]),
    'kafka_air_quality air_quality_events'[industrial_activity] = "moderate"
)
````
Estas medidas permiten desglosar cómo varía la calidad del aire en función del impacto industrial percibido en cada zona.

### 1. Descripción
Este análisis presenta una comparación entre tres niveles de actividad industrial y su relación con la calidad del aire. Se observan las variaciones en los promedios del AQI en función de la intensidad de la actividad industrial en distintas zonas urbanas.

El objetivo es detectar correlaciones entre la actividad económica industrial y la contaminación atmosférica, permitiendo identificar patrones de riesgo ambiental.

### 2. Datos Generales
Se utilizaron registros del sensor AQI combinados con un campo categórico llamado industrial_activity, clasificado como:
"high" (alta)
"moderate" (media)
"low" (baja)

El análisis se aplicó sobre datos agrupados por zonas: Industrial, Centro, Residencial y Suburbana

### 3. Distribución del AQI Industrial por Zona

### **Zona Industrial**
- Muestra los valores más altos en **AQI Alta Industria** y se confirma el fuerte impacto de la actividad fabril

### **Centro**
- Registra valores intermedios de **AQI Media Industria**,se supone que hay menos actividad industrial

### **Zona Residencial**
- Muestra valores moderados en **AQI Baja Industria**,pero con presencia detectable

### **Zona Suburbana**
- Muestra los valores más bajos en los tres indicadores

### 4. Interpretación de Resultados

Existe una correlación directa entre el nivel de actividad industrial y el aumento del AQI.
La contaminación generada por la industria no se limita exclusivamente a la zona de origen. Factores como los vientos, la topografía y el tráfico pueden transportar partículas contaminantes hacia otras zonas.
El análisis sugiere que las zonas residenciales cercanas a  estas zonas industriales están en riesgo indirecto.

### 5. Conclusiones 

A partir de los datos analizados, se proponen las siguientes acciones:

* Monitoreo ambiental continuo en zonas cercanas a polígonos industriales para evaluar el alcance real de la contaminación.

* Regulación de horarios de mayor producción industrial, para evitar la superposición con picos de actividad urbana (como horas punta de tráfico).

* Diseño de zonas de amortiguamiento entre áreas industriales y zonas residenciales mediante barreras vegetales, infraestructuras verdes o distancias mínimas reglamentadas.



### 6.3 Análisis del Impacto de Incendios en la Calidad del Aire (AQI) en Zona Suburbana

Este análisis tiene como objetivo cuantificar el efecto de los incendios forestales sobre el Índice de Calidad del Aire (AQI) específicamente en la zona suburbana, tradicionalmente caracterizada por su aire limpio y baja densidad de contaminación.

![image](https://github.com/user-attachments/assets/ffcc1651-a7e6-4f4f-8319-a426d9596614)

Para realizar esta comparación, se han realizado dos medidas que evalúan el AQI promedio con y sin presencia de incendios en la zona suburbana:

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

### 1. Descripción
Este gráfico compara el Índice de Calidad del Aire (AQI) promedio en la zona suburbana en dos escenarios distintos:cuando no hay incendios activos  y cuando  existen incendios forestales 

### 2. Datos Clave
- **AQI Sin Fuego**:Muestra la calidad del aire base en condiciones normales
- **AQI Con Fuego**:Refleja el deterioro de la calidad del aire durante incendios forestales

### 3. Hallazgos Principales

### **Condiciones Normales (Sin Fuego)**
- La zona suburbana mantiene un AQI bajo cuando no hay  incendios
- Corresponde a los valores más saludables del sistema de monitoreo

### **Durante Incendios (Con Fuego)**
- Se observa un incremento significativo del AQI
- El aumento puede ser de 5 a 10 veces el valor base según la  intensidad del fuego

### 4. Interpretación
 Aunque normalmente es la zona con mejor aire,la suburbana es la más afectada durante incendios forestales.
 Los incendios pueden causar un  deterioro rápido y severo de la calidad del aire y puede transformar el área suburbana en la más contaminada,dañando a la naturaleza y a su fauna

### 5. Conclusión
* Se podría implementar protocolos de emergencia ambiental para incendios en zonas suburbanas (alertas, evacuaciones, puntos limpios).
* Incrementar la densidad de sensores AQI temporales o móviles durante la temporada de incendios (especialmente verano).

### 6.4 Promedio de Vehículos por Minuto y AQI por Zona

En este gráfico se analiza la relación entre el volumen de tráfico vehicular y la calidad del aire (AQI) en cuatro zonas diferenciadas de Madrid: centro, residencial, suburbana e industrial. Se utilizan datos temporales para identificar patrones de contaminación vinculados a la actividad vehicular.

Creamos las siguientes medidas

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
El gráfico muestra dos métricas para cuatro zonas distintas (center, residential, suburb,industrial):  
- **Avg Vehículo Por Minuto**: Número promedio de vehículos que transitan cada cinco minutos.  
- **AOI Promedio por Zona**: Índice de Calidad del Aire (AQI) promedio en cada zona 

---

### 2. Datos Clave
- Zona center:  
  Se observan picos críticos de AQI (alrededor de 200) en los tramos horarios de 9:00, 14:00, 15:00 y 20:00.
Estos picos coinciden con horas de entrada/salida escolar y laboral.La alta densidad de tráfico en esas horas genera un aumento significativo en la concentración de contaminantes en el aire.
 
   ![image](https://github.com/user-attachments/assets/8765ecf5-cf39-4ea5-84a0-753ef89f4658) 

- Zonas residential
  El AQI se mantiene estable durante gran parte del día.Se identifican pequeñas subidas durante horas punta (especialmente entre las 18:00 y 20:00), posiblemente debido al regreso de personas del trabajo.El tráfico no es tan denso como en el centro, pero sigue teniendo un efecto notable.

![image](https://github.com/user-attachments/assets/f41301cc-3318-4480-97d8-f38ae7ad5374)

-  Zonas suburbana
  En la zona suburbana,se observa que el tráfico muy bajo,pero existen picos de AQI .
  La posible causa principal puede ser los incendios forestales ya que no coincide con aumentos de tráfico y es un fenómeno temporal.

 ![image](https://github.com/user-attachments/assets/cafbdca9-5887-4f9b-a82f-d55783fa4fbb)

- Zonas industriales
  En zonas industriales se observa un incremento del AQI durante el horario laboral (de 9:00 a 13:00 horas),lo que sugiere una correlación directa entre la actividad industrial y la contaminación del aire.

 ![image](https://github.com/user-attachments/assets/9575f8ef-099c-4694-ba67-dd5150ceddc5)


### 3. Interpretación de Resultados
Existe una correlación clara entre tráfico y AQI en las zonas centro y residencial.
En zonas industriales, el factor dominante es la actividad fabril, no el tráfico.
En zonas suburbanas, el AQI se ve afectado por eventos externos, como incendios, más que por el tránsito.

### 3. Conclusión
Se observa que en el centro de la ciudad,durante la primera hora de la mañana,el índice de calidad del aire (AQI) aumenta considerablemente.Esta subida podría estar relacionada con la entrada simultánea de los estudiantes al colegio,lo que genera un aumento en el tráfico y la actividad urbana.
Como posible solución,se propone implementar entradas escalonadas por curso en los colegios para evitar la acumulación de personas y vehículos a la misma hora.Del mismo modo,las empresas podrían adoptar horarios de entrada y salida más flexibles para sus empleados,lo que ayudaría a distribuir mejor el tráfico y reducir la contaminación en las horas punta.En la zona residencial también existen horas punta con mayor tránsito de vehículos, lo cual podría deberse a que muchas personas regresan del trabajo en ese horario.

Además,sería importante fomentar el uso del transporte público,la bicicleta y otros medios sostenibles,con el objetivo de disminuir la cantidad de vehículos particulares en circulación y,con ello,mejorar la calidad del aire en las zonas más afectadas.

---

![image](https://github.com/user-attachments/assets/ba3605f6-c018-4555-ab64-de2be18b5f09)


### 6.5 Distribución del AQI por Día de la Semana


![image](https://github.com/user-attachments/assets/d884f5c0-cead-4001-9309-25247056d76c)

Creamos una nueva columna
````
Día de la semana = 
VAR FechaConvertida = DATEVALUE(LEFT([ts], 10)) 
VAR FechaBase = DATE(YEAR(FechaConvertida), 1, 2)
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
Realizamos una nueva medida
````
AQI Promedio por Zona = 
AVERAGEX(
    VALUES('kafka_air_quality air_quality_events'[zone]),
    CALCULATE(AVERAGE('kafka_air_quality air_quality_events'[pollution_aqius]))
)
````
1. Descripción General
El gráfico muestra cómo varía el promedio del Índice de Calidad del Aire (AQI) a lo largo de los días de la semana .
Esto permite identificar posibles patrones de contaminación asociados a la actividad humana y la dinámica urbana durante la semana.

2. Datos Clave
* De lunes a viernes, los niveles de AQI son más elevados.Esto se relaciona con la mayor actividad vehicular y productiva típica de los días laborales.
Especialmente en zonas como el centro urbano y la zona industrial, los valores se intensifican.
* Los sábados y domingos se detecta una disminución significativa del AQI.El tráfico es menor, muchas industrias están inactivas y se reduce el movimiento de personas.Esta tendencia refuerza el vínculo entre la actividad humana y la contaminación ambiental.


3. Conclusión
Al analizar el AQI por día de la semana,se nota que la contaminación del aire es más alta de lunes a viernes y baja bastante los fines de semana.Esto muestra que la actividad diaria de las personas,como ir al trabajo o al colegio, influye mucho en la calidad del aire.
Los sábados y domingos,al haber menos movimiento y tráfico,el aire mejora.Por eso,sería buena idea pensar en medidas como horarios de entrada más escalonados o más teletrabajo para ayudar a reducir la contaminación en los días más cargados. También se podrían promover campañas de movilidad sostenible durante la semana, como “Miércoles sin coche” o “Jueves en bici”, e incrementar la presencia de sensores y sistemas de monitoreo en los días críticos.

De esta forma, se podrían tomar decisiones rápidas ante niveles elevados de AQI, como restringir el acceso de vehículos a determinadas zonas cuando se superen ciertos umbrales de contaminación.


## 7. Prometheus

En esta etapa,ponemos en marcha Prometheus para comenzar a recolectar métricas de nuestras fuentes configuradas.

1.Iniciar Prometheus

Vamos a su directorio ````/opt/prometheus-2.53.4 ````

Luego,arrancamos Prometheus usando nuestro archivo de configuración personalizado:
````
./prometheus --config.file=prometheus_proyecto_MLU.yml
````
2. Verificar Endpoints de Métricas
   
Una vez iniciado,comprobamos que nuestros endpoints están sirviendo correctamente las métricas:
````
curl http://localhost:11001/metrics
curl http://localhost:11002/metrics
curl http://localhost:11003/metrics
````
3. Confirmar Captura de Prometheus
   
Desde el navegador del host,accedemos a la interfaz de Prometheus:

````http://192.168.56.10:9090/targets````

4. Visualización

![image](https://github.com/user-attachments/assets/f661253c-c5f8-4228-8281-1dbf0f7d63a1)


![image](https://github.com/user-attachments/assets/d1eae758-eb03-4b81-be8c-effd0fe766f9)


## 8. Grafana

En este apartado instalamos y configuramos Grafana,la herramienta de visualización de métricas que se integra con Prometheus.

1. Instalación de Dependencias
   
Primero,instalamos los paquetes necesarios para que Grafana funcione correctamente:
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
   
Una vez iniciado el servicio,accedemos a Grafana desde el navegador web:
````
http://192.168.56.10:3000/dashboards
````
5. Visualización y Paneles
   
Creamos un dashboards,introduciendo un JSON ya dado y de esta manera podemos visualizar las métricas capturadas de forma gráfica.

![image](https://github.com/user-attachments/assets/fcf68def-b75a-40c5-adc7-cb9c5bd19d7d)

![image](https://github.com/user-attachments/assets/96508635-e8fa-4291-ba1f-1cd905c7d106)



### Opcional 
Creación de la tabla en MySQL

Podemos  crear una base de datos en MySQL junto con una tabla para almacenar los datos que se están generando.
Primero, accedemos a la consola de MySQL con privilegios de administrador utilizando el siguiente comando:
````
sudo mysql -u root -p
````
Una vez dentro, creamos una base de datos llamada kafka_air_quality que servirá como contenedor para las tablas relacionadas con nuestro proyecto:
````
CREATE DATABASE kafka_air_quality;
````

![image](https://github.com/user-attachments/assets/38af9f9c-adb3-466c-be61-fb6a4f90ee21)

Dentro de la base de datos,creamos la tabla air_quality_events.Esta tabla va a almacenar  toda la información capturada y procesada,con columnas que representan las diferentes variables de interés,tales como la calidad del aire,conteo de vehículos,presencia de incendios...:
````
CREATE TABLE air_quality_events (
    city VARCHAR(100),
    country VARCHAR(100),
    ts DATETIME,
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
    special_event VARCHAR(100)
);
````

![image](https://github.com/user-attachments/assets/112a9eec-10c7-47d0-ae86-0c5d33b21928)






























