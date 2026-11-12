def contar_saturacion(datos):
    """Devuelve cuántas veces aparecen el máximo y el mínimo de la señal."""
    maximo = datos.max()
    minimo = datos.min()
    conteo_maximo = (datos == maximo).sum()
    conteo_minimo = (datos == minimo).sum()
    return conteo_maximo, conteo_minimo

def calcular_duracion(muestras, rate):
    '''
    Para convertir la gráfica en una representación auditiva, es necesario saber el rate + muestras
    la duracion sera igual a muestas / rate 
    '''
    #rate -> HZ de onda
    # Nº de muestras: una muestra es una medición puntual,
    # un solo número que el sensor registra en un instante.
    duracion = muestras / rate
    return duracion
