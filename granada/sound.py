import numpy as np
from scipy.io.wavfile import write


def normalizar(datos):
    """Escala la señal para que su valor más grande en magnitud sea 1.

    Recibe un array de numpy y devuelve otro array (float) con valores entre -1 y 1.
    """
    pico = np.abs(datos).max()
    return datos / pico

def convertir_enteros(datos):
    """Convierte la señal normalizada a enteros de 16 bits.

    Recibe un array con valores entre -1 y 1 y devuelve un array de tipo int16 con valores entre -32767 y 32767.
    Lanza ValueError si algún valor está fuera de [-1, 1].
    """
    pico = np.abs(datos).max()
    if pico > 1:
        raise ValueError(f"Los datos no están normalizados: el valor máximo en magnitud es {pico}")
    senal_wav = datos * 32767
    return senal_wav.astype(np.int16)

def escribir_wav(ruta, rate, datos):
    """Guarda una señal de 16 bits como archivo WAV.

    Recibe la ruta del archivo, la frecuencia de muestreo del WAV (entero) y un array int16.
    No devuelve nada: crea el archivo en disco.
    """
    write(ruta, rate, datos)
