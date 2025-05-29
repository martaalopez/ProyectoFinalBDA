# Proyecto Final BDA 2024-25

 <!-- ![ChatGPT Image 26 abr 2025, 12_03_57](https://github.com/user-attachments/assets/6102e595-1fdc-4c95-bc74-89ab9ad7bd9c)
-->
## 1.Introducción

Hoy en dia la calidad del aire y la contaminacion son factores ambientales muy preocupantes en nuestra sociedad .El trafico  diario de vehiculos ,tanto de personas que van al trabajo como de padres q van a llevar a sus hijos al colegio son factores que hacen que aumente  el deterioro de la calidad de aire.
Además algunos fenómenos naturales como los incendios forestales pueden tener un fuerte impacto en la contaminación atmosférica,al igual que la actividad industrial,donde las emisiones de humo y partículas contaminantes se mezclan con la atmósfera, empeorando aún más la situación.

Esto puede hacer que existan consecuencias directas en la salud publica, un articulo  revela que 2000 niños mueren cada dia en el mundo por mal calidad del aire,por ello he decidido hacer una investigación que se enfoca en el monitoreo y análisis de los principales factores que afectan la calidad del aire, con el objetivo de identificar los eventos más frecuentes y críticos. A partir de estos datos, espero poder extraer conclusiones que contribuyan a diseñar soluciones eficientes para combatir este grave problema global.
  

## 2.Fuente de Informacion

Para poder abarcar con todo esto vamos a apoyarnos en los datos proporcionados  por la AirVisual API la cual  ofrece información sobre el tiempo, la calidad del aire y los incendios activos,etc...
Sin embargo, esta API presenta un problema:los datos se actualizan cada hora ,mientras que nuestro objetivo es realizar un monitoreo en tiempo real, actualizando los datos cada segundo.

Por ello vamos a generar  unos datos sinteticos,  incluyendo no solo las variables básicas ofrecidas por la API, sino también otros datos adicionales que considero relevantes para un análisis más completo,como el tráfico, la actividad industrial y la probabilidad de incendios.
Los datos ficticios se recogerán desde sensores virtuales distribuidos en cuatro zonas distintas de Madrid:
Centro: Zona con alto volumen de tráfico, ideal para observar el impacto del tránsito urbano.
Residencial: Área con menor densidad de vehículos, donde se espera una menor contaminación.
Industrial: Región con alta actividad industrial, donde predominan los contaminantes derivados del humo y procesos fabriles.
Suburbana: Zonas periféricas con mezcla de factores naturales y urbanos, y mayor probabilidad de incendios forestales.
Tenemos además varias condiciones para que podemos simular bien nuestros datos y se acerquen lo más posible a la realidad.
Gracias por la aclaración. Vamos a tener en cuenta esta lógica en la simulación. Aquí te resumo todas las condiciones actuales que se usan para generar los datos sintéticos en tu script de Python:

---

1. Horario de simulación

   * Comienza a las 12:00 del mediodía.
   * En nuestra simulación,cada 3 segundos en tiempo real equivalen a 1 minuto en tiempo simulado.

2. **Condiciones de tráfico por hora**

   * Horas punta: 8, 9, 14, 15, 20 (más tráfico).
   * Menos tráfico en fines de semana.
   * Tráfico normal fuera de horas punta.

3. Zonas diferenciadas

   * `residential`, `industrial`, `center`, `suburb` con distintos factores:

     * `traffic_factor`, `fire_probability`, `industry_factor`, `vehicle_rate`.

4. Vehículos

   * Cantidad depende del `vehicle_rate` por zona.
   * Aumenta el conteo acumulado de vehículos en cada paso.

5. Fuegos

   * Ocurren aleatoriamente según `fire_probability`.
   * Duración entre 3 y 10 minutos, dependiendo de la zona.
   * Influyen en el aumento del AQI.
   * En las zonas suburbanas es más probable que se origine un incendio

6. AQI (calidad del aire)

   * Cambia en cada paso según:

     * Fuegos (intensidad: `low`, `medium`, `high`).
     * Tráfico (proporcional al número de vehículos).
     * Actividad industrial.
     * Entre las 12:00 y las 14:00: aumento **lento** (1-3 puntos si hay tráfico).
     * A partir de las 14:00: aumento **más rápido** (por tráfico postlaboral).

7. Eventos especiales añadidos

   * Ej: partidos de fútbol o conciertos en el centro.
   * Aumentan el tráfico de forma significativa y afectan negativamente al AQI.
   * En las zonas industriales y suburbanas no hay eventos especiales.

8. Accidentes de tráfico añadidos

   * Ocurren aleatoriamente con una baja probabilidad.
   * Aumentan el tráfico en la zona afectada.
   * Causan subida rápida del AQI por atascos.

## 3. Requisitos
Debe haber como mínimo 3 nodos en los clusters (en cada uno):
Hadoop (HDFS/Yarn)

![image](https://github.com/user-attachments/assets/bbe8c104-5059-4658-88ab-952a1f15c1cb)

![image](https://github.com/user-attachments/assets/ee90e9d2-2931-43d7-b1bb-297e8eb30cb9)


Spark
![image](https://github.com/user-attachments/assets/4a360f4a-3007-4646-92e2-289e0c5d676c)


Kafka
Hemos actualizado nuestro kafka a la versión 4.0.0

![image](https://github.com/user-attachments/assets/1d2feb40-6772-4ea7-9e3f-e7edf1420f69)


## 4.Configuración del Clúster de Kafka 
1.Vamos a establecer todos los archivos de configuración en una carpeta  llamada proyectoBDA_MLU, que en mi caso estará alojada en /opt/kafka/proyecto_MLU

![image](https://github.com/user-attachments/assets/e12ef486-f0bd-4ca7-b4fa-3a83788f20b7)

Creamos los directorios necesarios para nuestro proyecto_MLU

````
mkdir -p /opt/kafka/proyecto_MLU/config
mkdir -p /opt/kafka/proyecto_MLU/logs
````

En nuestra arquitectura vamos a tener lo siguiente:
Un controller que va a ser el nodo responsable de poder coordinal el clúster.Se va a encargar de gestionar los eventos como la creación y eliminación de topics,la asignaciñon de paerticiones y la detección de fallos en los brokers.
Para el controller, debemos usar como base la configuración de propiedades de controller de kafka que se encuentran config/controller.properties

Dos brokers,donde cada uno va a estar identificado por un Id y va a contener ciertas particiones de un topic.va a permitir replicar y poder particionar dichos topics balanceando la carga de almacenamiento entre los brokers.Esto perimite q kafka sea tolerante a fallos y escalable.
Para cada broker, necesitaremos crear un archivo de configuración por separado. Para ello debemos usar como base la configuración de propiedades de brokers de kafka que se encuentran config//broker.properties

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

## 5.Levantamos sistemas 
Vamos a activar todos los servicios para que nuestro flujo de datos pueda funcionar de manera correcta.

## 5.1 Levantamos HDFS (Hadoop Distributed File System)
Levantamos HDFS que será nuestro sistema de almacenamiento distribuido,donde los datos procesados se guardarán.
````
cd $HADOOP_HOME
stop-dfs.sh
start-dfs.sh

# Verificamos que el sistema no este en modo seguro 
hdfs dfsadmin -safemode get
hdfs dfsadmin -safemode leave
````
## 5.2 Arrancamos Spark Master y Workers
Lanzamos spark master y los workers del cluster.
Spark va a ser el encargado de leer los datos desde kafka y poder analizarlos en tiempo real.
````
/opt/hadoop-3.4.1/spark-3.5.4/sbin/start-master.sh
/opt/hadoop-3.4.1/spark-3.5.4/sbin/start-workers.sh
````

````
/opt/hadoop-3.4.1/spark-3.5.4/sbin/stop-all.sh
sleep 5
/opt/hadoop-3.4.1/spark-3.5.4/sbin/start-all.sh
````

## 5.3 Iniciamos Kafka (Controller + Brokers)
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
## 5.4 Creamos el Topic Kafka
Creamos el topic  llamado air-quality con factor de replica 2 y 4 particiones ya que en nuestros datos sintécticos vamos a coger los datos de 4 zonas distintas de la ciudad. Cada partición va a manejar los datos y los eventos específicos de cada zona.
````
/opt/kafka_2.13-4.0.0/bin/kafka-topics.sh --create --topic air-quality --bootstrap-server 192.168.11.10:9094 --replication-factor 2 --partitions 4
````
Para eliminar el topic si es necesario:
````
/opt/kafka_2.13-4.0.0/bin/kafka-topics.sh --delete --bootstrap-server 192.168.11.10:9094 --topic  air-quality
````
Verificación
````
/opt/kafka_2.13-4.0.0/bin/kafka-topics.sh --list --bootstrap-server 192.168.11.10:9094
````
![image](https://github.com/user-attachments/assets/1ae0aafe-e850-437c-a781-9aa21d2dc3ba)


## 5.6 Creación del producer y del consumer
Vamos a crear el productor Kafka que simula datos recogidos por sensores distribuidos en las 4 zonas de Madrid ,más tarde lo ejecutaremos.
Déspues necesitamos un consumer que lea los eventos del topic air-quality. Este consumer está implementado en PySpark Structured Streaming para poder analizar los datos de forma continua y reactiva.
El consumer :
Lee el flujo de mensajes desde Kafka.
Extrae y estructura los datos JSON recibidos.
Imprime un resumen por microbatch en consola.
Para facilitar la conexión con Power BI,además de almacenar los datos en HDFS,hemos creado una tabla en MySQL.Esto nos permite guardar y actualizar los datos generados de forma más sencilla y accesible para herramientas de análisis.

## 5.6.1 Creación de la tabla en MYSQL
````
sudo mysql -u root -p
````
Creamos la base de datos
````
CREATE DATABASE kafka_air_quality;
````

![image](https://github.com/user-attachments/assets/38af9f9c-adb3-466c-be61-fb6a4f90ee21)

Creamos la tabla
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



## 5.7 Ejecutamos el Consumer
Este paso debe hacerse antes del producer,ya que el consumer necesita estar escuchando el stream desde el principio para no perder datos.

````
PYTHONPATH=$HOME/.local/lib/python3.10/site-packages spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 --master spark://192.168.11.10:7077 /opt/kafka/proyecto_MLU/data_stream/consumer.py
````
## 5.8 Ejecutamos el Producer Kafka
Lanzamos el productor
````
python3 /opt/kafka/proyecto_MLU/data_stream/producer.py
````
## 5.9 Visualizamos la información

Aprovecharemos la Consumer API de Kafka para ver está consumiendo los datos correctamente una vez lanzada la aplicación
````
/opt/kafka_2.13-4.0.0/bin/kafka-console-consumer.sh --topic air-quality --from-beginning --bootstrap-server 192.168.11.10:9094
````
Para ver los archivos generados en HDFS

````
hdfs dfs -ls /opt/kafka/proyecto_MLU/data/
````
![image](https://github.com/user-attachments/assets/baca4845-0b2b-4fcb-9ee1-004e7e53dcd1)

Visualización web del sistema de archivos HDFS:

http://192.168.56.10:9870/explorer.html

![image](https://github.com/user-attachments/assets/eb74a8c9-18de-4be6-85c3-ced1ca068ade)


````
cp /opt/kafka_2.13-4.0.0/bin/kafka-server-start.sh /opt/kafka_2.13-4.0.0/bin/kafka-server-start_proyecto_MLU.sh
````
Visualizamos que los datos se han guardado en nuestra base de datos de Mysql 

![image](https://github.com/user-attachments/assets/39c16059-7e8e-44f0-ba78-a850521f9fe3)

Creamos 
````
nano /opt/kafka_2.13-4.0.0/bin/kafka-server-start_proyecto_MLU.sh
````
cp /opt/prometheus-2.53.4/prometheus.yml /opt/prometheus-2.53.4/prometheus_proyecto_MLU.yml

````
nano /opt/prometheus-2.53.4/prometheus_proyecto_MLU.yml
````


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
## 6.Visualización en PowerBI
En este apartado,abordaremos el proceso para conectar con PowerBI con nuestra base de datos MYSQL con el fin de realizar un análisis visual dinámico de los datos almacenados.

* Conexión de PowerBI con la base de datos MYSQL
Para comenzar abrimos PowerBI y seleccionamos la opción de conectamos a una base de datos MySQL.Esta conexión nos permitirá extraer los datos necesarios directamente desde nuestra base,asegurando que los informes reflejen siempre la información más reciente.

![image](https://github.com/user-attachments/assets/db769c6b-aeda-4546-96c7-e8ee26775ad9)

* Introducimos nuestra IP donde se encuentra alojada nuestra base de datos MYSQL ,así como el nombre  específico de nuestra base de datos que queremos consultar.Además tendremos que introducir nuestro usuario y contraseña.

![image](https://github.com/user-attachments/assets/03825a69-aae7-4101-bef5-f0def19f6b8a)

## 6.1 Promedio de AQI

![image](https://github.com/user-attachments/assets/544aaaba-3959-4da6-853d-dd6b1b6088a7)

## 1. Descripción
Se presentan los datos sobre el Índice de Calidad del Aire (AQI) promedio y su distribución porcentual en cuatro zonas distintas de Madrid, obtenidos a través de un sistema de monitoreo en tiempo real con datos sintéticos.

## 2. Datos Generales
El análisis revela marcadas diferencias en la calidad del aire entre las zonas monitoreadas:
- Las zonas **industrial** y **centro** concentran aproximadamente el 66.45% del AQI total combinado (33.25% y 33.2% respectivamente).
- La zona **residencial** contribuye con el 14.68% del AQI total.
- La zona **suburbana** muestra el menor impacto, con valores mínimos de contaminación.

## 3. Distribución de Contaminación por Zona
Los datos demuestran claramente cómo los factores urbanos e industriales afectan la calidad del aire:
- **Zona Industrial (33.25%, AQI ≈163)**: Presenta los valores más altos, directamente vinculados a la actividad fabril y emisiones industriales.
- **Centro (33.2%, AQI ≈163)**: Muestra niveles similares a la zona industrial, atribuibles al intenso tráfico vehicular y alta densidad urbana.
- **Residencial (14.68%, AQI ≈72)**: Exhibe niveles moderados, reflejando menor actividad contaminante pero aún afectada por el entorno urbano.
- **Suburbana (AQI ≈9)**: Registra la mejor calidad de aire, beneficiada por menor densidad poblacional y mayor presencia de áreas verdes.

## 4. Interpretación de Resultados
Este patrón de distribución confirma las hipótesis iniciales del proyecto:
1. **Impacto de la actividad humana**: Las zonas con mayor intervención antropogénica (industrial y centro) muestran claramente los peores indicadores.
2. **Efecto del tráfico vehicular**: La similitud entre centro e industrial sugiere que el tráfico puede ser tan contaminante como la actividad industrial.
3. **Beneficios de la planificación urbana**: La zona residencial, aunque urbana, muestra valores significativamente mejores, posiblemente por mejor planificación y menores factores contaminantes.
4. **Ventajas de las áreas periféricas**: La zona suburbana confirma que alejarse de los núcleos urbanos principales mejora notablemente la calidad del aire.

Estos resultados subrayan la necesidad de políticas diferenciadas por zona:
- Medidas estrictas de control de emisiones industriales
- Restricciones de tráfico en el centro urbano
- Incentivos para mantener bajos los niveles en zonas residenciales
- Protección de las áreas suburbanas como pulmones urbanos

El sistema implementado demuestra ser efectivo para identificar patrones espaciales de contaminación, permitiendo una toma de decisiones basada en datos en tiempo cuasi-real.

## 6.2 Análisis de Calidad del Aire (AQI) en Zonas Industriales

![image](https://github.com/user-attachments/assets/1e0466c1-0bd8-4bcd-b98e-ed48cce9cc14)


## 1. Descripción
Este gráfico presenta tres métricas clave de calidad del aire (AQI) específicamente relacionadas con zonas industriales: AQI Alta Industria, AQI Baja Industria y AQI Media Industria, desglosadas por diferentes zonas urbanas.

## 2. Datos Generales
El análisis muestra cómo varía el impacto industrial en la calidad del aire según la zona:
- Se comparan tres indicadores de contaminación industrial (alta, baja y media)
- Las zonas analizadas incluyen: industrial, centro, residencial y suburbana

## 3. Distribución del AQI Industrial por Zona

### **Zona Industrial**
- Muestra los valores más extremos en **AQI Alta Industria**, confirmando el fuerte impacto de la actividad fabril
- Presenta también variación significativa entre AQI Alta y Baja Industria, indicando fluctuaciones según horarios de producción

### **Centro**
- Registra valores intermedios de **AQI Media Industria**, sugiriendo contaminación industrial transportada
- Posible efecto combinado de emisiones locales y contaminantes industriales arrastrados por el viento

### **Zona Residencial**
- Exhibe valores moderados en **AQI Baja Industria**, pero con presencia detectable
- Indica que la contaminación industrial afecta áreas circundantes, aunque en menor medida

### **Zona Suburbana**
- Muestra los valores más bajos en los tres indicadores
- Confirma que es la menos afectada por emisiones industriales directas

## 4. Interpretación de Resultados

1. **Impacto geográfico de la industria**: La contaminación industrial no se limita a su zona de origen, sino que se extiende a áreas vecinas.

2. **Variabilidad temporal**: La diferencia entre AQI Alta y Baja Industria sugiere que:
   - Los picos de producción industrial generan contaminación aguda
   - Existen momentos de menor impacto (noches, fines de semana)

3. **Transporte de contaminantes**: Los valores en zona centro indican que:
   - Los contaminantes industriales viajan por la atmósfera
   - Se combinan con otras fuentes de polución urbana

4. **Efecto protector de la distancia**: La zona suburbana demuestra cómo el alejamiento geográfico reduce la exposición a contaminantes industriales.

## 5. Conclusiones Operativas

- **Para autoridades**:
  - Necesidad de monitoreo continuo en zonas aledañas a polos industriales
  - Establecer protocolos para episodios de AQI Alta Industria
  - Regular horarios de máxima producción contaminante

- **Para urbanistas**:
  - Mantener suficiente distancia entre zonas industriales y residenciales
  - Considerar patrones de viento predominantes en la planificación urbana

- **Para ciudadanos**:
  - Informar sobre variaciones horarias de calidad del aire
  - Recomendar precauciones en episodios de AQI Alta Industria

## 6.3 Análisis del Impacto de Incendios en la Calidad del Aire (AQI) en Zona Suburbana

![image](https://github.com/user-attachments/assets/ffcc1651-a7e6-4f4f-8319-a426d9596614)

## 1. Descripción
Este gráfico compara el Índice de Calidad del Aire (AQI) promedio en la zona suburbana en dos escenarios distintos: cuando no hay incendios activos (Avg AQI Sin Fuego) y cuando existen incendios forestales (Avg AQI Con Fuego).

## 2. Datos Clave
- **AQI Sin Fuego**: Muestra la calidad del aire base en condiciones normales
- **AQI Con Fuego**: Refleja el deterioro de la calidad del aire durante incendios forestales

## 3. Hallazgos Principales

### **Condiciones Normales (Sin Fuego)**
- La zona suburbana mantiene un AQI bajo en ausencia de incendios
- Corresponde a los valores más saludables del sistema de monitoreo
- Refleja los beneficios de:
  - Menor densidad poblacional
  - Mayor vegetación
  - Alejamiento de fuentes contaminantes urbanas

### **Durante Incendios (Con Fuego)**
- Se observa un incremento significativo del AQI
- El aumento puede ser de 5 a 10 veces el valor base (según intensidad del fuego)
- Factores que contribuyen:
  - Emisión directa de partículas PM2.5 y PM10
  - Generación de hollín y cenizas
  - Transporte de contaminantes por el viento

## 4. Interpretación

1. **Vulnerabilidad ambiental**: Aunque normalmente es la zona con mejor aire, la suburbana es la más afectada durante incendios forestales.

2. **Efecto agudo**: Los incendios causan deterioro rápido y severo de la calidad del aire, transformando temporalmente el área suburbana en la más contaminada.

3. **Duración del impacto**: Los efectos pueden persistir días después de controlado el incendio, especialmente por material particulado residual.

## 5. Recomendaciones

- **Sistema de alerta temprana**: Implementar protocolos específicos para incendios en áreas suburbanas
- **Monitoreo reforzado**: Aumentar la densidad de sensores durante la temporada de incendios
- **Plan de contingencia**:
  - Mascarillas N95 para población vulnerable
  - Recomendaciones de permanecer en interiores
  - Cierre preventivo de escuelas en áreas afectadas
- **Prevención**:
  - Mantenimiento de cortafuegos
  - Campañas de concienciación sobre riesgo de incendios
  - Restricciones a actividades que puedan generar chispas en épocas de riesgo

Este análisis demuestra que, aunque la zona suburbana disfruta normalmente de la mejor calidad del aire, es precisamente la más vulnerable a los efectos catastróficos de los incendios forestales, requiriendo estrategias específicas de protección.























