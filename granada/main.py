from analysis import calcular_duracion, contar_saturacion
from read import obtener_sismograma
from sound import convertir_enteros, escribir_wav, normalizar

traza = obtener_sismograma()

#array de numpy
datos = traza[0].data

## Análisis de la muestra
conteo_maximo, conteo_minimo = contar_saturacion(datos)

print(f"Número de veces que aparece el máximo: {conteo_maximo}")
print(f"Número de veces que aparece el mínimo: {conteo_minimo}")

rate = traza[0].stats.sampling_rate
muestras = traza[0].stats.npts

duracion = calcular_duracion(muestras, rate)
print(f"Su duración es de: {duracion:.1f} segundos")

# Normalización de datos y verificación
normalizar_datos = normalizar(datos)
valor_mas_alto = normalizar_datos.max()
valor_mas_bajo = normalizar_datos.min()
tipo_de_numero = normalizar_datos.dtype

print(f"Valor mas alto normalizado: {valor_mas_alto}")
print(f"Valor mas bajo normalizado: {valor_mas_bajo}")
print(f"Tipo de numero: {tipo_de_numero}")

## Verificación de la conversión a WAV
senal_wav = convertir_enteros(normalizar_datos)
valor_mas_alto_wav = senal_wav.max()
valor_mas_bajo_wav = senal_wav.min()
tipo_de_numero_wav = senal_wav.dtype

print(f"Valor mas alto: {valor_mas_alto_wav}")
print(f"Valor mas bajo: {valor_mas_bajo_wav}")
print(f"Tipo de numero: {tipo_de_numero_wav}")

## Obtener representación auditiva WAV
escribir_wav("sonido/terremoto-4000rate.wav", 4000, senal_wav)

## LA ESTACIÓN ESCOGIDA (ARMILLA) MIDE SOLO ACELERACIÓN
## SU REPRESENTACION AUDITIVA SERÁ PARECIDA A UN GOLPE SECO
