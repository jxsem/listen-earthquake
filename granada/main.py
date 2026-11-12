import argparse
import sys
from pathlib import Path

from obspy.clients.fdsn.header import FDSNException

from granada.analysis import calcular_duracion, contar_saturacion
from granada.figure import guardar_figura
from granada.read import crear_cliente, obtener_sismograma
from granada.sound import convertir_enteros, escribir_wav, normalizar

RATE_WAV = 4000
CARPETA_SONIDO = Path(__file__).parent / "sonido"
CARPETA_FIGURA = Path(__file__).parent / "sismograma"


def main(estacion):
    try:
        client = crear_cliente()
        traza = obtener_sismograma(client, estacion)
    except FDSNException as error:
        print(f"Error al hablar con el IGN: {error}")
        sys.exit(1)

    CARPETA_FIGURA.mkdir(exist_ok=True)
    guardar_figura(traza, CARPETA_FIGURA / f"sismograma-{estacion}.png")

    # array de numpy
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
    datos_normalizados = normalizar(datos)
    valor_mas_alto = datos_normalizados.max()
    valor_mas_bajo = datos_normalizados.min()
    tipo_de_numero = datos_normalizados.dtype

    print(f"Valor mas alto normalizado: {valor_mas_alto}")
    print(f"Valor mas bajo normalizado: {valor_mas_bajo}")
    print(f"Tipo de numero: {tipo_de_numero}")

    ## Verificación de la conversión a WAV
    senal_wav = convertir_enteros(datos_normalizados)
    valor_mas_alto_wav = senal_wav.max()
    valor_mas_bajo_wav = senal_wav.min()
    tipo_de_numero_wav = senal_wav.dtype

    print(f"Valor mas alto: {valor_mas_alto_wav}")
    print(f"Valor mas bajo: {valor_mas_bajo_wav}")
    print(f"Tipo de numero: {tipo_de_numero_wav}")

    ## Obtener representación auditiva WAV
    CARPETA_SONIDO.mkdir(exist_ok=True)
    escribir_wav(CARPETA_SONIDO / f"terremoto-{estacion}-{RATE_WAV}rate.wav", RATE_WAV, senal_wav)

    ## LA ESTACIÓN ESCOGIDA (ARMILLA) MIDE SOLO ACELERACIÓN
    ## SU REPRESENTACION AUDITIVA SERÁ PARECIDA A UN GOLPE SECO


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sonifica el terremoto de Granada para una estación del IGN.")
    parser.add_argument("estacion", nargs="?", default="EXARM", help="código de la estación (por defecto EXARM)")
    argumentos = parser.parse_args()
    main(argumentos.estacion)
