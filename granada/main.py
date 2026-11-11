from read import obtener_sismograma

traza = obtener_sismograma()

print(traza)
print(type(traza[0]))

## Comprueba cuales son los máximos y mínimos del sismograma
array_data = traza[0].data

maximo = array_data.max()
minimo = array_data.min()

print("Maximo:",maximo)
print("Minimo:",minimo)

## Verifica si la señal está saturada contando máximos y mínimos
conteo_maximo = (array_data == maximo).sum()
conteo_minimo = (array_data == minimo).sum()

print("Maximos:",conteo_maximo)
print("Minimos:",conteo_minimo)

'''
Para convertir la gráfica en una representación audiovisual, es necesario saber el rate + muestas
la duracion sera igual a muestas / rate 
'''
#rate -> HZ de onda
# Nº de muestras: una muestra es una medición puntual,
# un solo número que el sensor registra en un instante.
rate = traza[0].stats.sampling_rate
numero_muestras = traza[0].stats.npts
duracion = numero_muestras / rate
print(f"Rate: {rate}") #rate -> HZ de onda
print(f"Nº muestras: {numero_muestras}") 
print(f"Duracion {duracion:.1f}s")
