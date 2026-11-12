# Sonificación del terremoto de Granada (14-08-2026)

Convierte la señal de un sismómetro en un fichero de audio (WAV) y en una figura, para **oír** un terremoto y comparar cómo cambia según la distancia al epicentro.

Proyecto de aprendizaje en Python (ObsPy, NumPy, SciPy).

## El evento

- Terremoto M 5.0, a 1 km al oeste de Alhendín (Granada).
- 2026-08-14, 23:04:40 UTC (01:04:40 hora de Madrid del día 15). Fuente: USGS.
- Epicentro usado en el código: 37.1076 N, 3.6456 W (coordenadas de Google Maps; el USGS da 37.109 N, 3.664 W, unos 1,6 km de diferencia).

## Qué hace

1. Descarga los datos de forma de onda del servicio FDSN del **IGN** (red `ES`).
2. Analiza la traza (duración, veces que aparecen el máximo y el mínimo).
3. Normaliza la señal dividiéndola entre su pico y la convierte a enteros de 16 bits.
4. Escribe un WAV a 4000 Hz (la señal original es de 200 Hz, así que suena 20 veces más rápida y más aguda: 100 s pasan a 5 s).
5. Guarda el sismograma como PNG.

## Estaciones comparadas

Las dos son acelerómetros (`HNZ`, componente vertical), a 200 Hz y con 20001 muestras en la misma ventana (23:04:20 – 23:06:00 UTC).

| Estación | Zona | Distancia | Sonido (se genera al ejecutar) | Figura |
|---|---|---|---|---|
| EXARM | Armilla | 4,0 km | `granada/sonido/terremoto-EXARM-4000rate.wav` | `granada/sismograma/sismograma-EXARM.png` |
| EXMAZ | Murcia | 213,8 km | `granada/sonido/terremoto-EXMAZ-4000rate.wav` | `granada/sismograma/sismograma-EXMAZ.png` |

La estación más lejana con datos no es la primera de la lista: EXMU (216,1 km) aparecía en el inventario con `HN?`, pero `get_waveforms` devolvió «sin datos» (HTTP 204), así que se descartó.

## Resultados

Observado:

- La señal llega a Armilla hacia las 23:04:41 y a EXMAZ hacia las 23:05:15.
- En Armilla la energía se concentra en unos pocos segundos. En EXMAZ aparece más tarde y se mantiene durante mucho más tiempo.
- En el audio de Armilla se oye un golpe seco. En el de EXMAZ, un siseo previo, dos golpes y un sonido sostenido, parecido a un trueno.

Interpretación (hipótesis, no verificada):

- Una onda sísmica rápida (P) y otra más lenta (S) viajan a velocidades distintas, así que la separación entre ellas crece con la distancia. Con velocidades típicas (P ≈ 6 km/s, S ≈ 3,5 km/s) se esperarían unos 25 s de separación a 214 km (~1,3 s tras acelerar el audio). **Pendiente de comprobar** ampliando el gráfico alrededor de 23:05:10–23:05:50.
- Al normalizar, ambos sonidos tienen el mismo volumen máximo, así que la distancia se oye en el tiempo y no en la intensidad.

## Cómo ejecutarlo

Requiere Python 3 y conexión a internet (se consulta el IGN).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m granada.main            # estación cercana (EXARM, por defecto)
python -m granada.main EXMAZ      # estación lejana
```

Los WAV no se versionan: se crean en `granada/sonido/` al ejecutar. Los PNG sí están en el repositorio.

Se ejecuta desde la raíz del repositorio y con `-m`, porque el código usa imports de paquete (`from granada.read import ...`). El argumento es el código de la estación; los ficheros de salida llevan ese código en el nombre. El canal (`HNZ`) es la constante `CANAL` de `granada/read.py`.

## Estructura

| Fichero | Responsabilidad |
|---|---|
| `granada/stations.py` | Busca estaciones cerca del epicentro y calcula su distancia |
| `granada/read.py` | Lista canales y descarga la traza del IGN |
| `granada/analysis.py` | Duración y recuento del máximo y el mínimo |
| `granada/sound.py` | Normalización, conversión a 16 bits y escritura del WAV |
| `granada/figure.py` | Dibuja y guarda el sismograma |
| `granada/velocity.py` | Experimento: integra la aceleración para obtener velocidad |
| `granada/main.py` | Orquesta todo el proceso |

## Limitaciones

- Solo se comparan dos estaciones: es una observación, no una conclusión general.
- Las señales están en cuentas del digitalizador. No se ha aplicado la respuesta instrumental para pasar a m/s², así que las amplitudes de las dos estaciones no son comparables en unidades físicas.
- Los tiempos de llegada de P y S salen de velocidades medias supuestas, no de un modelo de la corteza.
- El servicio del IGN falla de forma intermitente (por ejemplo, 504). El código distingue «sin datos» de «sin servicio», pero no reintenta ni guarda la traza en disco.
- Faltan tests automáticos.
