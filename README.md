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
 Vamos a tener en cuenta esta lógica en la simulación. 

---

* Horario de simulación
El sistema inicia la simulación a las 9:00 de la mañana del día 1 de enero de 2025. Cada segundo en el mundo real representa un minuto en el tiempo simulado, por lo tanto, cada iteración genera datos nuevos que reflejan las condiciones en cada zona con una altísima frecuencia temporal. Esto permite realizar un análisis casi en tiempo real.

* Condiciones de tráfico
Las condiciones del tráfico son un factor importante para el cálculo del AQI (índice de calidad del aire). Se tienen en cuenta dos aspectos principales: el día de la semana y la hora del día.

Durante los días de semana, se considera que hay horas punta (a las 8, 9, 14, 15 y 20 horas), donde el tráfico es más denso. Durante los fines de semana, el tráfico disminuye notablemente. Si el momento actual de la simulación coincide con una hora punta en día laborable, se clasifica como condición de tráfico “peak”; si es fin de semana, se clasifica como “weekend”, y en los demás casos como “normal”.

Cada zona reacciona de manera diferente a estas condiciones. Por ejemplo, en el centro de Madrid se registra un mayor número de vehículos durante las horas punta, mientras que en zonas suburbanas la variación es mínima.

* Conteo y acumulación de vehículos
En cada paso de la simulación, se genera un número aleatorio de vehículos que han pasado por cada zona, en función de su densidad de tráfico y la condición actual (hora punta o no). Este número se acumula en un contador que representa el total de vehículos presentes en la zona.

Para evitar una acumulación infinita, se aplica una “decadencia” que simula el hecho de que algunos vehículos abandonan la zona con el tiempo. Este mecanismo permite mantener una representación realista del flujo vehicular.

* Incendios forestales y urbanos
Los incendios son otro factor crítico en esta simulación. Cada zona tiene asignada una probabilidad específica de que ocurra un incendio. Por ejemplo, en las zonas suburbanas, esta probabilidad es significativamente mayor, ya que se simula una mayor cercanía a entornos forestales.

Cuando ocurre un incendio, se le asigna una duración (en minutos simulados) y una intensidad (baja, media o alta). Durante el tiempo que dure el incendio, el AQI de esa zona aumenta dependiendo de la intensidad. Una vez transcurrido el tiempo, el incendio se considera extinguido y se restablece el estado de normalidad.

* Eventos especiales
Solo en la zona centro se simulan eventos especiales como conciertos y partidos de fútbol. Estos eventos están programados para horas específicas del día: a las 18:00 se celebra un concierto, y a las 20:00 un partido de fútbol. Cuando ocurre uno de estos eventos, se incrementa drásticamente el número de vehículos en la zona y se eleva el AQI debido al aumento del tráfico.

* Accidentes de tráfico
Otro factor inesperado y aleatorio introducido en la simulación son los accidentes de tráfico. Su probabilidad de ocurrencia es baja, pero se incrementa ligeramente en la zona centro debido a su alta densidad de tránsito. Si ocurre un accidente, el AQI se ve afectado negativamente, simulando el efecto de los atascos y la congestión prolongada.

Cálculo del índice AQI
El AQI se ajusta dinámicamente en cada paso de la simulación. Parte de un valor inicial entre 40 y 70 para cada zona, y luego cambia en función de los siguientes factores:

Penalización por horas punta.

Número de vehículos acumulados en la zona.

Existencia e intensidad de incendios.

Presencia de eventos especiales.

Actividad industrial.

Ocurrencia de accidentes.

Además, se aplican límites para evitar valores irreales. El AQI nunca baja de 10 ni sube de 200. En condiciones normales (sin incendios, ni eventos, ni horas punta), se tiende a estabilizar por debajo de 100, excepto en zonas como el centro donde la actividad constante puede llevarlo a valores más altos.



## 3. Requisitos
Debe haber como mínimo 3 nodos en los clusters (en cada uno):
Hadoop (HDFS/Yarn)

Hadoop es el sistema responsable del almacenamiento distribuido de grandes volúmenes de datos (HDFS) y de la gestión de recursos y ejecución de tareas distribuidas (YARN).

Contar con al menos tres nodos en el cluster Hadoop permite:

Distribuir los datos entre múltiples máquinas (DataNodes).

Mantener un nodo maestro (NameNode) que coordina la lectura y escritura en el sistema de archivos.

Asegurar la replicación de los datos en diferentes nodos para prevenir pérdidas en caso de fallos.

Esto permite una infraestructura resiliente, escalable y tolerante a errores.
![image](https://github.com/user-attachments/assets/bbe8c104-5059-4658-88ab-952a1f15c1cb)

![image](https://github.com/user-attachments/assets/ee90e9d2-2931-43d7-b1bb-297e8eb30cb9)


Spark
Apache Spark es el motor encargado del procesamiento distribuido de los datos. A diferencia de Hadoop MapReduce, Spark permite trabajar en memoria, lo que lo hace mucho más rápido y eficiente para el análisis de grandes volúmenes de datos.

Tener tres nodos como mínimo en el cluster Spark ofrece varias ventajas:

Distribución paralela del procesamiento.

Coordinación de tareas desde el nodo maestro (Driver).

Ejecución simultánea de trabajos en los nodos trabajadores (Workers).

Mejora del rendimiento y la robustez del sistema frente a posibles fallos.
![image](https://github.com/user-attachments/assets/4a360f4a-3007-4646-92e2-289e0c5d676c)


Kafka
Apache Kafka es la tecnología utilizada para gestionar el flujo de mensajes en tiempo real. En este proyecto, Kafka se encarga de transmitir los eventos generados por los sensores virtuales (como los datos de calidad del aire, tráfico, incendios, etc.).

Se ha actualizado Kafka a la versión 4.0.0, lo que introduce una mejora importante: la eliminación de la dependencia de Zookeeper, gracias al nuevo sistema de metadatos KRaft (Kafka Raft Metadata mode).

Para Kafka, un cluster de al menos tres nodos es esencial para:

Garantizar la replicación de mensajes entre distintos brokers.

Mantener un quorum en el consenso distribuido, tanto con Zookeeper (en versiones antiguas) como con KRaft.

Asegurar la persistencia de los datos y la disponibilidad del sistema frente a fallos.
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
Se inician los servicios del NameNode y los DataNodes, permitiendo el almacenamiento distribuido de grandes volúmenes de datos.
Se activa YARN, que gestionará los recursos y la ejecución de procesos en los distintos nodos del clúster.
Esto asegura que todo lo que se procese o almacene posteriormente tenga soporte escalable y tolerante a fallos.
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
Activamos el Spark Master y varios Spark Workers para permitir el procesamiento en paralelo de grandes cantidades de datos.
Spark será el encargado de consumir los datos desde Kafka y transformarlos, analizarlos o agregarlos en tiempo real.
Esta etapa garantiza que tengamos la capacidad computacional necesaria para realizar análisis complejos y responder con rapidez.
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
En esta fase, procedemos a la creación del tópico principal de Kafka donde se publicarán todos los eventos generados por nuestro productor de datos en tiempo real. Este tópico se denominará air-quality, ya que su función será centralizar la información relacionada con la calidad del aire, tráfico, incendios y eventos especiales en distintas zonas de la ciudad.

Dado que nuestra simulación abarca cuatro zonas geográficas distintas de Madrid (centro, residencial, industrial y suburbana), decidimos configurar el tópico con 4 particiones, de manera que cada una pueda gestionar de forma paralela y eficiente los eventos específicos de una zona. Esto mejora el rendimiento del sistema, permite mayor paralelización en el consumo de datos y facilita una asignación lógica de responsabilidades entre los consumidores.
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


## 5.6 Creación del producer y del consumer
Vamos a crear el productor Kafka que es el componente encargado de simular la generación de datos que normalmente serían capturados por sensores distribuidos en las cuatro zonas de Madrid: centro, residencial, industrial y suburbana. Este productor, implementado en Python, genera eventos sintéticos que incluyen variables como la calidad del aire, el conteo de vehículos, incendios activos y eventos especiales, y los envía en tiempo real al tópico air-quality de Kafka.

Este proceso simula el comportamiento de sensores reales que envían datos periódicos, permitiéndonos realizar pruebas y análisis de manera controlada y repetible.
Déspues necesitamos un consumer que lea los eventos del topic air-quality. Este consumer está implementado en PySpark Structured Streaming para poder analizar los datos de forma continua y reactiva.
El consumer :
Lee el flujo de mensajes desde Kafka.
Extrae y estructura los datos JSON recibidos.
Imprime un resumen por microbatch en consola.
Para facilitar la conexión con Power BI,además de almacenar los datos en HDFS,hemos creado una tabla en MySQL.Esto nos permite guardar y actualizar los datos generados de forma más sencilla y accesible para herramientas de análisis.

## 5.6.1 Creación de la tabla en MYSQL

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



## 5.7 Ejecutamos el Consumer

Es fundamental iniciar el consumidor antes de poner en marcha el productor. Esto asegura que el consumer esté activo desde el inicio del flujo de datos y no se pierda ninguna información emitida por el productor.
Para ejecutar el consumidor utilizamos spark-submit con las librerías necesarias para conectar Spark con Kafka. El comando es el siguiente:

````
PYTHONPATH=$HOME/.local/lib/python3.10/site-packages spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 --master spark://192.168.11.10:7077 /opt/kafka/proyecto_MLU/data_stream/consumer.py
````
## 5.8 Ejecutamos el Producer Kafka

Una vez que el consumidor está corriendo y escuchando el stream, procedemos a iniciar el productor. El producer simula la generación y envío de datos sintéticos desde las distintas zonas de la ciudad, alimentando el flujo que será consumido y analizado.
Para lanzar el productor ejecutamos:
````
python3 /opt/kafka/proyecto_MLU/data_stream/producer.py
````
Este script comenzará a enviar los eventos generados al topic Kafka, dando inicio a la simulación y procesamiento de datos.

## 5.9 Visualizamos la información

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

 ## 7.Prometehus

 Para implementarlo debemos de 

 Para monitorear nuestro sistema, vamos a configurar Prometheus específicamente para nuestro proyecto. Los pasos son los siguientes:
 
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

![image](https://github.com/user-attachments/assets/f661253c-c5f8-4228-8281-1dbf0f7d63a1)
























