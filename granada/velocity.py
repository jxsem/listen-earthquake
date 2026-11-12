import sys

from obspy.clients.fdsn.header import FDSNException

from granada.main import CARPETA_SONIDO, RATE_WAV
from granada.read import crear_cliente, obtener_sismograma
from granada.sound import convertir_enteros, escribir_wav, normalizar

# integrate(): suma el área acumulada bajo la curva de la señal a lo largo del tiempo.
# La traza mide aceleración (en cuentas, sin aplicar la respuesta instrumental),
# así que al integrar una vez se obtiene "velocidad" en cuentas·s, NO en m/s.

# Hipótesis:
# - Un M5 a ~4 km: la energía llega de golpe y se acaba pronto.
# - Duración de la parte fuerte: ~15–20 s reales que pasan a ~1 s con ×20.


def main():
    try:
        client = crear_cliente()
        traza = obtener_sismograma(client)
    except FDSNException as error:
        print(f"Error al hablar con el IGN: {error}")
        sys.exit(1)

    copia = traza[0].copy()
    copia.integrate()

    # se normaliza
    datos_normalizados = normalizar(copia.data)
    # se convierte
    datos_wav = convertir_enteros(datos_normalizados)
    # se escribe
    CARPETA_SONIDO.mkdir(exist_ok=True)
    escribir_wav(CARPETA_SONIDO / "terremoto-velocidad.wav", RATE_WAV, datos_wav)


if __name__ == "__main__":
    main()
