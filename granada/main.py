from analysis import calcular_duracion, contar_saturacion
from read import obtener_sismograma

traza = obtener_sismograma()

#array de numpy
datos = traza[0].data

conteo_maximo, conteo_minimo = contar_saturacion(datos)

print(f"Número de veces que aparece el máximo: {conteo_maximo}")
print(f"Número de veces que aparece el mínimo: {conteo_minimo}")

rate = traza[0].stats.sampling_rate
muestras = traza[0].stats.npts

duracion = calcular_duracion(muestras, rate)
print(f"Su duración es de: {duracion:.1f} segundos")