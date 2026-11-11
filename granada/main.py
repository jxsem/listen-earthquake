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
