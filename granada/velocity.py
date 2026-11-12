from read import obtener_sismograma
from sound import normalizar, convertir_enteros, escribir_wav

traza = obtener_sismograma()
copia = traza[0].copy()
copia.integrate()

#se normaliza
datos_normalizados = normalizar(copia.data)
#se convierte
datos_wav = convertir_enteros(datos_normalizados)
#se escribe
escribir_wav("sonido/terremoto-velocidad.wav", 4000, datos_wav)

""" Hipótesis:
- Un M5 a ~4 km: la energía llega de golpe y se acaba pronto.
- Duración de la parte fuerte: ~15–20 s reales que pasan a ~1 s con ×20.
"""
