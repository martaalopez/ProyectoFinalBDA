# Proyecto Final BDA 2024-25

![ChatGPT Image 26 abr 2025, 12_03_57](https://github.com/user-attachments/assets/6102e595-1fdc-4c95-bc74-89ab9ad7bd9c)

*1.Introducción
Hoy en dia la calidad del aire y la contaminacion son factores ambientales muy preocupantes en nuestra sociedad .El trafico  diario de vehiculos ,tanto de personas que van al trabajo como de padres q van a llevar a sus hijos al colegio son factores que hacen que aumente  el deterioro de la calidad de aire.
Además algunos fenómenos naturales como los incendios forestales pueden tener un fuerte impacto en la contaminación atmosférica,al igual que la actividad industrial,donde las emisiones de humo y partículas contaminantes se mezclan con la atmósfera, empeorando aún más la situación.

Esto puede hacer que existan consecuencias directas en la salud publica, un articulo  revela que 2000 niños mueren cada dia en el mundo por mal calidad del aire,por ello he decidido hacer una investigación que se enfoca en el monitoreo y análisis de los principales factores que afectan la calidad del aire, con el objetivo de identificar los eventos más frecuentes y críticos. A partir de estos datos, espero poder extraer conclusiones que contribuyan a diseñar soluciones eficientes para combatir este grave problema global.
  
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

2.Fuente de Informacion

Para poder abarcar con todo esto vamos a apoyarnos en los datos proporcionados  por la AirVisual API la cual  ofrece información sobre el tiempo, la calidad del aire y los incendios activos,etc...
Sin embargo, esta API presenta un problema:los datos se actualizan cada hora , mientras que nuestro objetivo es realizar un monitoreo en tiempo real, actualizando los datos cada minuto.

Por ello vamos a generar  unos datos sintetcios,  incluyendo no solo las variables básicas ofrecidas por la API, sino también otros datos adicionales que considero relevantes para un análisis más completo:
En terminos generales tendriamos estos datos
-Casos de enfermedades respiratorias detectadas por minuto.
-Número de vehículos circulando en la vía pública.
-Información sobre incendios activos.
-Nivel de actividad industrial.
-Calidad del aire (AQI) y contaminante principal (mainus).
-Lugar

2.1 Estructura de datos 
En este apartado vamos a especificar la estructura 
