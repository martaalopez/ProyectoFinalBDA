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

La versión que tenemos actualmente es la 3.9.0 tenemos que actulizarla a la 4.0.0 para ello 






